"""
项目管理 API —— 保存/搜索/导出/版本管理轮系数据

数据库: SQLite (backend/app/data/gear_projects.db)
"""
import io
import json
import sqlite3
from pathlib import Path
from datetime import datetime, date
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

router = APIRouter()

DB_DIR = Path(__file__).resolve().parent.parent / "data"
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / "gear_projects.db"


def get_db():
    """获取数据库连接"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """初始化数据库表"""
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            version TEXT DEFAULT '01',
            customer TEXT DEFAULT '',
            project_code TEXT DEFAULT '',
            date_created TEXT DEFAULT (date('now')),
            date_modified TEXT DEFAULT (date('now')),
            info_json TEXT DEFAULT '{}',
            data_json TEXT DEFAULT '{}',
            notes TEXT DEFAULT ''
        )
    """)
    conn.commit()
    conn.close()


init_db()


# ===== 文件编号生成 =====

@router.get("/projects/next-file-no")
def get_next_file_no(version: str = Query("01", description="版本号，用于拼接显示名")):
    """生成下一个文件编号。格式: {日期}{序数}-{版本}
    序数规则: 今日新建文档数目，版本升级不消耗新序数，删除的序数可复用。
    """
    today = date.today().strftime("%Y%m%d")
    conn = get_db()
    rows = conn.execute(
        "SELECT id, name, project_code, version, info_json FROM projects ORDER BY id"
    ).fetchall()
    conn.close()

    # 按 file_no 分组（file_no = 日期 + 序数，例如 "2026080901"）
    file_no_groups = {}  # file_no -> [versions]
    for r in rows:
        try:
            info = json.loads(r["info_json"] or "{}")
        except:
            info = {}
        fn = info.get("file_no", "") or r["project_code"] or r["name"]
        if fn and len(fn) >= 10 and fn[:8] == today:
            prefix = fn[:10]  # 日期8位 + 序数2位
            if prefix not in file_no_groups:
                file_no_groups[prefix] = set()
            file_no_groups[prefix].add(r["version"])

    # 找到最小的可用序数（01-99），优先复用已删除的号
    used_nums = {int(k[8:10]) for k in file_no_groups}
    seq = 1
    while seq <= 99:
        if seq not in used_nums:
            break
        seq += 1

    if seq > 99:
        raise HTTPException(status_code=400, detail="今日文档数已达上限（99）")

    file_no = f"{today}{seq:02d}"
    return {"file_no": file_no, "display_name": f"{file_no}-{version}"}


# ===== 请求/响应模型 =====

class ProjectSaveRequest(BaseModel):
    name: str
    version: str = "01"
    customer: str = ""
    project_code: str = ""
    form_info: dict = {}
    pulleys: list = []
    belt_params: dict = {}
    tensioner: dict = {}
    notes: str = ""


class ProjectUpdateRequest(BaseModel):
    name: Optional[str] = None
    version: Optional[str] = None
    customer: Optional[str] = None
    project_code: Optional[str] = None
    form_info: Optional[dict] = None
    pulleys: Optional[list] = None
    belt_params: Optional[dict] = None
    tensioner: Optional[dict] = None
    notes: Optional[str] = None


# ===== API 端点 =====

@router.post("/projects")
def save_project(data: ProjectSaveRequest):
    """保存项目——同文件编号+版本覆盖更新"""
    conn = get_db()
    today = date.today().isoformat()
    info_json = json.dumps(data.form_info, ensure_ascii=False)
    data_json = json.dumps({
        "pulleys": data.pulleys,
        "belt_params": data.belt_params,
        "tensioner": data.tensioner
    }, ensure_ascii=False)

    file_no = data.form_info.get("file_no", "")
    version = data.version or "01"

    # 检查是否已存在同 file_no + version 的记录
    existing_id = None
    if file_no:
        rows = conn.execute(
            "SELECT id, info_json FROM projects WHERE version = ? ORDER BY date_modified DESC",
            (version,)
        ).fetchall()
        for r in rows:
            try:
                info = json.loads(r["info_json"] or "{}")
                if info.get("file_no") == file_no:
                    existing_id = r["id"]
                    break
            except:
                pass

    if existing_id:
        conn.execute(
            """UPDATE projects SET name=?, customer=?, project_code=?,
               date_modified=?, info_json=?, data_json=?, notes=?
               WHERE id=?""",
            (data.name, data.customer, data.project_code,
             today, info_json, data_json, data.notes, existing_id)
        )
        conn.commit()
        conn.close()
        return {"id": existing_id, "message": "更新成功（已覆盖同版本）"}

    cursor = conn.execute(
        """INSERT INTO projects (name, version, customer, project_code,
           date_created, date_modified, info_json, data_json, notes)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (data.name, data.version, data.customer, data.project_code,
         today, today, info_json, data_json, data.notes)
    )
    conn.commit()
    project_id = cursor.lastrowid
    conn.close()
    return {"id": project_id, "message": "保存成功"}


@router.get("/projects")
def list_projects(
    keyword: str = Query("", description="搜索关键词（文件编号/客户/项目代码）"),
    version: str = Query("", description="版本筛选"),
    customer: str = Query("", description="客户筛选"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0)
):
    """搜索/列出项目——按文件编号去重合并，返回所有版本"""
    conn = get_db()
    rows = conn.execute(
        "SELECT id, name, version, customer, project_code, date_created, date_modified, notes, info_json, data_json "
        "FROM projects ORDER BY date_modified DESC"
    ).fetchall()
    conn.close()

    # 提取 file_no 并去重合并
    groups = {}  # file_no -> {info, versions}
    order = []

    for r in rows:
        try:
            info = json.loads(r["info_json"] or "{}")
        except:
            info = {}
        try:
            data_json = json.loads(r["data_json"] or "{}")
        except:
            data_json = {}
        belt = data_json.get("belt_params", {})
        file_no = info.get("file_no", "") or r["project_code"] or r["name"]
        if not file_no:
            file_no = f"UNNAMED_{r['id']}"

        ver = r["version"] or "01"

        if file_no not in groups:
            groups[file_no] = {
                "file_no": file_no,
                "name": r["name"],
                "customer": r["customer"],
                "project_code": r["project_code"],
                "date_modified": r["date_modified"],
                "notes": r["notes"],
                "versions": [],
                "ids": {},  # version -> id mapping
                "version_details": {}  # version -> per-version metadata
            }
            order.append(file_no)

        if ver not in (v for v in groups[file_no]["versions"]):
            groups[file_no]["versions"].append(ver)
        groups[file_no]["ids"][ver] = r["id"]
        groups[file_no]["version_details"][ver] = {
            "name": r["name"],
            "project_code": r["project_code"],
            "date_modified": r["date_modified"],
            "notes": r["notes"] or "",
            "layers": info.get("layers", ""),
            "ribs": belt.get("ribs") or belt.get("rib_type", "").replace("PK", ""),
            "cord_material": belt.get("cord_material") or belt.get("belt_material", ""),
            "effective_length": belt.get("effective_length")
        }
        # Keep latest modified date
        if r["date_modified"] > groups[file_no]["date_modified"]:
            groups[file_no]["date_modified"] = r["date_modified"]
            groups[file_no]["name"] = r["name"]
            groups[file_no]["customer"] = r["customer"]
            groups[file_no]["project_code"] = r["project_code"]

    # 筛选
    filtered = []
    for file_no in order:
        g = groups[file_no]
        if keyword:
            kw = keyword.lower()
            if not (kw in g["file_no"].lower() or kw in g["customer"].lower()
                    or kw in g["project_code"].lower()):
                continue
        if customer and customer.lower() not in g["customer"].lower():
            continue
        if version and version not in g["versions"]:
            continue
        filtered.append(g)

    total = len(filtered)
    paginated = filtered[offset:offset + limit]

    return {"total": total, "projects": paginated}


@router.get("/projects/versions")
def list_versions():
    """列出所有已有版本（供筛选下拉）"""
    conn = get_db()
    rows = conn.execute(
        "SELECT DISTINCT version FROM projects WHERE version != '' ORDER BY version DESC"
    ).fetchall()
    conn.close()
    return {"versions": [r["version"] for r in rows]}


@router.get("/projects/customers")
def list_customers():
    """列出所有已有客户（供筛选下拉）"""
    conn = get_db()
    rows = conn.execute(
        "SELECT DISTINCT customer FROM projects WHERE customer != '' ORDER BY customer"
    ).fetchall()
    conn.close()
    return {"customers": [r["customer"] for r in rows]}


@router.get("/projects/by-file")
def get_project_by_file(
    file_no: str = Query(...),
    version: str = Query("01")
):
    """通过文件编号 + 版本获取项目"""
    conn = get_db()
    # 查找 info_json 中 file_no 匹配的记录
    rows = conn.execute(
        "SELECT id, info_json FROM projects ORDER BY date_modified DESC"
    ).fetchall()
    target_id = None
    for r in rows:
        try:
            info = json.loads(r["info_json"] or "{}")
            if info.get("file_no") == file_no and r["id"] not in (target_id or ()):
                target_id = r["id"]
                break
        except:
            pass
    if not target_id:
        # fallback: search by file_no exact match
        for r in rows:
            try:
                info = json.loads(r["info_json"] or "{}")
                if info.get("file_no") == file_no:
                    target_id = r["id"]
                    break
            except:
                pass
    if not target_id:
        conn.close()
        raise HTTPException(status_code=404, detail="项目不存在")

    row = conn.execute("SELECT * FROM projects WHERE id = ?", (target_id,)).fetchone()
    conn.close()

    data = dict(row)
    data["form_info"] = json.loads(data.get("info_json", "{}"))
    data_json = json.loads(data.get("data_json", "{}"))
    data["pulleys"] = data_json.get("pulleys", [])
    data["belt_params"] = data_json.get("belt_params", {})
    data["tensioner"] = data_json.get("tensioner", {})
    return data


@router.get("/projects/{project_id}")
def get_project(project_id: int):
    """获取单个项目详情（含所有数据）"""
    conn = get_db()
    row = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="项目不存在")
    data = dict(row)
    data["form_info"] = json.loads(data.get("info_json", "{}"))
    data_json = json.loads(data.get("data_json", "{}"))
    data["pulleys"] = data_json.get("pulleys", [])
    data["belt_params"] = data_json.get("belt_params", {})
    data["tensioner"] = data_json.get("tensioner", {})
    return data


@router.put("/projects/{project_id}")
def update_project(project_id: int, data: ProjectUpdateRequest):
    """更新项目"""
    conn = get_db()
    row = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="项目不存在")

    updates = {}
    if data.name is not None:
        updates["name"] = data.name
    if data.version is not None:
        updates["version"] = data.version
    if data.customer is not None:
        updates["customer"] = data.customer
    if data.project_code is not None:
        updates["project_code"] = data.project_code
    if data.notes is not None:
        updates["notes"] = data.notes
    if data.form_info is not None:
        updates["info_json"] = json.dumps(data.form_info, ensure_ascii=False)
    if data.pulleys is not None or data.belt_params is not None or data.tensioner is not None:
        existing_data = json.loads(row["data_json"])
        if data.pulleys is not None:
            existing_data["pulleys"] = data.pulleys
        if data.belt_params is not None:
            existing_data["belt_params"] = data.belt_params
        if data.tensioner is not None:
            existing_data["tensioner"] = data.tensioner
        updates["data_json"] = json.dumps(existing_data, ensure_ascii=False)

    updates["date_modified"] = date.today().isoformat()

    if updates:
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [project_id]
        conn.execute(f"UPDATE projects SET {set_clause} WHERE id = ?", values)
        conn.commit()

    conn.close()
    return {"message": "更新成功"}


@router.delete("/projects/{project_id}")
def delete_project(project_id: int):
    """删除项目"""
    conn = get_db()
    row = conn.execute("SELECT id FROM projects WHERE id = ?", (project_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="项目不存在")
    conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    conn.commit()
    conn.close()
    return {"message": "已删除"}


@router.post("/projects/{project_id}/export")
def export_project(project_id: int):
    """导出单个项目为 Excel（基于 REPORT.xlsx 模板）"""
    import openpyxl

    conn = get_db()
    row = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="项目不存在")

    data = dict(row)
    form_info = json.loads(data.get("info_json", "{}"))
    data_json = json.loads(data.get("data_json", "{}"))
    pulleys = data_json.get("pulleys", [])
    belt_params = data_json.get("belt_params", {})
    tensioner = data_json.get("tensioner", {})
    conn.close()

    # 加载模板
    template_path = DB_DIR.parent.parent.parent / "REPORT.xlsx"
    if not template_path.exists():
        raise HTTPException(status_code=500, detail="模板文件不存在")

    wb = openpyxl.load_workbook(str(template_path))
    ws = wb["EN_REPORT"]

    # 插入 Logo（替换 gear_logo.png 即可换图标）
    logo_path = template_path.parent / "frontend" / "public" / "images" / "gear_logo.png"
    if logo_path.exists():
        img = openpyxl.drawing.image.Image(str(logo_path))
        img.width, img.height = 192.5, 55
        ws.add_image(img, "A1")

    def _fill(cell, val, default=""):
        c = ws[cell]
        # 跳过合并单元格的非左上角位置
        for mr in ws.merged_cells.ranges:
            if c.coordinate in mr:
                if c.row != mr.min_row or c.column != mr.min_col:
                    return
        c.value = val if val not in (None, "") else default

    def _fmt(v, prec=2):
        if v is None or v == "": return ""
        try: return round(float(v), prec)
        except: return v

    # Page 1 fills (same as report.py)
    _fill("E5", form_info.get("file_no", ""))
    _fill("L5", form_info.get("version", data.get("version", "")))
    _fill("Q5", form_info.get("date", date.today().isoformat()))
    _fill("F10", form_info.get("customer", data.get("customer", "")))
    _fill("R10", form_info.get("project", data.get("project_code", "")))
    _fill("J11", str(form_info.get("cylinders", "")))
    _fill("R11", str(form_info.get("power", "")))
    _fill("H12", form_info.get("problem_statement", ""))
    _fill("H13", form_info.get("analysis_reference", ""))
    _fill("J35", belt_params.get("belt_name", "Multi- V Belt"))
    _fill("J36", belt_params.get("rib_type", ""))
    mat = belt_params.get("belt_material", "").lower()
    _fill("K36", "Neoprene" if mat in ("cr", "neoprene") else ("EPDM" if mat == "epdm" else ""))
    _fill("U36", _fmt(belt_params.get("belt_height")))
    _fill("J37", str(belt_params.get("ribs", "")))
    _fill("K37", belt_params.get("cord_material", ""))
    _fill("U37", _fmt(belt_params.get("flat_to_pitch")))
    sw = belt_params.get("stretch_wear_allow")
    _fill("I38", f"≤ {sw}" if sw is not None else "")
    _fill("U38", _fmt(belt_params.get("pitch_to_effective")))
    _fill("J42", tensioner.get("type", ""))
    _fill("U42", _fmt(tensioner.get("arm_length")))
    _fill("I43", _fmt(tensioner.get("pivot_x")))
    _fill("L43", _fmt(tensioner.get("pivot_y")))
    _fill("U43", _fmt(tensioner.get("angle")))
    _fill("I44", _fmt(tensioner.get("design_tension")))
    _fill("U44", _fmt(tensioner.get("spring_stiffness")))

    # Pulley table
    for i in range(10):
        r = 50 + i
        if i < len(pulleys):
            p = pulleys[i]
            is_na = p.get("type") == "none" or p.get("code") == "NA"
            _fill(f"E{r}", "" if is_na else p.get("code", ""))
            _fill(f"H{r}", "" if is_na else _fmt(p.get("x")))
            _fill(f"K{r}", "" if is_na else _fmt(p.get("y")))
            _fill(f"N{r}", "/" if p.get("type") == "groove" else (_fmt(p.get("flat_dia")) if p.get("type") == "flat" else ""))
            _fill(f"Q{r}", "" if is_na else _fmt(p.get("pitch_dia")))
            _fill(f"T{r}", "" if is_na else _fmt(p.get("effective_dia")))
            _fill(f"W{r}", "Flat" if p.get("type") == "flat" else ("Grooved" if p.get("type") == "groove" else ""))
        else:
            for col in ["E", "H", "K", "N", "Q", "T", "W"]:
                _fill(f"{col}{r}", "")

    # Results
    _fill("J110", _fmt(belt_params.get("effective_length")))
    _fill("K111", _fmt(belt_params.get("length_tolerance")))
    _fill("I115", _fmt(tensioner.get("torque")))
    _fill("U116", _fmt(tensioner.get("angle")))
    dt = tensioner.get("design_tension")
    ribs = belt_params.get("ribs")
    if dt is not None and ribs and ribs > 0:
        _fill("U111", round(dt / ribs, 2))

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    wb.close()

    # 生成 ASCII 安全的文件名 + UTF-8 编码版本（兼容中文）
    from urllib.parse import quote
    raw_name = f"{data.get('name', 'Report')}_v{data.get('version', '01')}.xlsx"
    safe_name = ''.join(c if ord(c) < 128 else '_' for c in raw_name)
    quoted_name = f"attachment; filename=\"{safe_name}\"; filename*=UTF-8''{quote(raw_name)}"
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": quoted_name}
    )
