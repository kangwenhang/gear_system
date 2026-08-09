"""
Excel 报告生成 API —— 读取 REPORT.xlsx 模板 + 填充数据

POST /api/generate-report
接收前端 sharedStore 数据，填充 REPORT.xlsx 模板各单元格，返回 xlsx 文件下载。
"""
import io
import copy
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

router = APIRouter()

# 模板路径
TEMPLATE_PATH = Path(__file__).resolve().parent.parent.parent.parent / "REPORT.xlsx"


# ===== 请求数据模型 =====
class PulleyData(BaseModel):
    code: str = ""
    name: str = ""
    type: str = ""  # groove / flat / none
    x: Optional[float] = None
    y: Optional[float] = None
    pitch_dia: Optional[float] = None
    effective_dia: Optional[float] = None
    flat_dia: Optional[float] = None
    rotation: int = 1

class BeltParams(BaseModel):
    belt_name: str = ""
    belt_type: str = ""
    rib_type: str = ""
    belt_material: str = ""
    cord_material: str = ""
    ribs: Optional[int] = None
    belt_height: Optional[float] = None
    stretch_wear_allow: Optional[float] = None
    flat_to_pitch: Optional[float] = None
    pitch_to_effective: Optional[float] = None
    effective_length: Optional[float] = None
    length_tolerance: Optional[float] = None

class TensionerData(BaseModel):
    type: str = "Automatic"
    torque: Optional[float] = None
    angle: Optional[float] = None
    arm_length: Optional[float] = None
    pivot_x: Optional[float] = None
    pivot_y: Optional[float] = None
    spring_stiffness: Optional[float] = None
    design_tension: Optional[float] = None

class FormInfo(BaseModel):
    file_no: str = ""
    version: str = ""
    date: str = ""
    customer: str = ""
    project: str = ""
    cylinders: Optional[str] = None
    power: Optional[str] = None
    problem_statement: str = ""
    analysis_reference: str = ""

class ReportRequest(BaseModel):
    form_info: FormInfo
    pulleys: List[PulleyData] = []
    belt_params: BeltParams
    tensioner: TensionerData


# ===== 辅助函数 =====
def _fmt(val, default="", precision=2):
    """格式化数值"""
    if val is None or val == "":
        return default
    try:
        return round(float(val), precision)
    except (ValueError, TypeError):
        return val

def _fill_cell(ws, cell_ref, value):
    """填充单元格，跳过合并单元格的非左上角位置"""
    cell = ws[cell_ref]
    # 检查是否是合并单元格的非左上角（只读）
    for merged_range in ws.merged_cells.ranges:
        if cell.coordinate in merged_range:
            # 只有左上角可写
            if cell.row != merged_range.min_row or cell.column != merged_range.min_col:
                return  # 跳过非左上角的合并单元格
    cell.value = value


@router.post("/generate-report")
def generate_report(data: ReportRequest):
    """
    根据 REPORT.xlsx 模板填充数据，返回生成的 xlsx 文件
    """
    if not TEMPLATE_PATH.exists():
        raise HTTPException(status_code=500, detail=f"模板文件不存在: {TEMPLATE_PATH}")

    import openpyxl
    from openpyxl.drawing.image import Image as XLImage

    # 加载模板
    wb = openpyxl.load_workbook(str(TEMPLATE_PATH))
    ws = wb["EN_REPORT"]

    # 插入 Logo（替换 gear_logo.png 即可换图标）
    logo_path = TEMPLATE_PATH.parent / "frontend" / "public" / "images" / "gear_logo.png"
    if logo_path.exists():
        img = XLImage(str(logo_path))
        img.width, img.height = 192.5, 55
        ws.add_image(img, "A1")


    fi = data.form_info
    bp = data.belt_params
    tn = data.tensioner
    pls = data.pulleys

    # ==================== 第一页：Project Information ====================

    # File No / Version / Date (row 5)
    _fill_cell(ws, "E5", fi.file_no or "")
    _fill_cell(ws, "L5", fi.version or "")
    _fill_cell(ws, "Q5", fi.date or datetime.now().strftime("%Y-%m-%d"))

    # Client / Project (row 10)
    _fill_cell(ws, "F10", fi.customer or "")
    _fill_cell(ws, "R10", fi.project or "")

    # Cylinders / Power (row 11)
    _fill_cell(ws, "J11", fi.cylinders or "")
    power_val = fi.power
    if power_val:
        _fill_cell(ws, "R11", power_val)
    else:
        _fill_cell(ws, "R11", "")

    # Problem Statement (row 12)
    _fill_cell(ws, "H12", fi.problem_statement or "")

    # Analysis Reference (row 13)
    _fill_cell(ws, "H13", fi.analysis_reference or "")

    # ==================== Belt Data (input) ====================

    # Belt name (row 35)
    _fill_cell(ws, "J35", bp.belt_name or bp.belt_type or "Multi- V Belt")

    # Rib type & Material (row 36)
    rib_val = bp.rib_type or ""
    mat_val = bp.belt_material or ""
    if mat_val.lower() == "epdm":
        _fill_cell(ws, "K36", "EPDM")
    elif mat_val.lower() == "cr" or mat_val.lower() == "neoprene":
        _fill_cell(ws, "K36", "Neoprene")
    # Belt Height
    _fill_cell(ws, "U36", _fmt(bp.belt_height))

    # Ribs / Cord Material (row 37)
    _fill_cell(ws, "J37", _fmt(bp.ribs, precision=0))
    _fill_cell(ws, "K37", bp.cord_material or "")
    # Flat to Pitch
    _fill_cell(ws, "U37", _fmt(bp.flat_to_pitch))

    # Stretch & Wear Allow (row 38)
    sw = bp.stretch_wear_allow
    _fill_cell(ws, "I38", f"≤ {sw}" if sw is not None else "")
    # Pitch to Effective
    _fill_cell(ws, "U38", _fmt(bp.pitch_to_effective))

    # ==================== Tensioner Data (input) ====================

    # Type (row 42)
    _fill_cell(ws, "J42", tn.type or "Automatic")
    # Arm Length
    _fill_cell(ws, "U42", _fmt(tn.arm_length))

    # Pivot Point (row 43)
    _fill_cell(ws, "I43", _fmt(tn.pivot_x))
    _fill_cell(ws, "L43", _fmt(tn.pivot_y))
    # Arm Angle
    _fill_cell(ws, "U43", _fmt(tn.angle))

    # Design Tension (row 44)
    _fill_cell(ws, "I44", _fmt(tn.design_tension))
    # Spring Rate
    _fill_cell(ws, "U44", _fmt(tn.spring_stiffness))

    # ==================== Layout Data (input) — Pulley Table (rows 50-59) ====================

    for i in range(10):
        row = 50 + i
        if i < len(pls):
            p = pls[i]
            is_na = p.type == "none" or p.code == "NA"
            _fill_cell(ws, f"E{row}", "" if is_na else (p.code or ""))
            _fill_cell(ws, f"H{row}", "" if is_na else _fmt(p.x))
            _fill_cell(ws, f"K{row}", "" if is_na else _fmt(p.y))
            # Flat Diameter: groove → "/", flat → flat_dia, none → ""
            if p.type == "groove":
                _fill_cell(ws, f"N{row}", "/")
            elif p.type == "flat":
                _fill_cell(ws, f"N{row}", _fmt(p.flat_dia))
            else:
                _fill_cell(ws, f"N{row}", "")
            # Pitch Diameter
            _fill_cell(ws, f"Q{row}", "" if is_na else _fmt(p.pitch_dia))
            # Effective Diameter
            _fill_cell(ws, f"T{row}", "" if is_na else _fmt(p.effective_dia))
            # Type
            if p.type == "flat":
                _fill_cell(ws, f"W{row}", "Flat")
            elif p.type == "groove":
                _fill_cell(ws, f"W{row}", "Grooved")
            else:
                _fill_cell(ws, f"W{row}", "")
        else:
            # Empty rows
            for col in ["E", "H", "K", "N", "Q", "T", "W"]:
                _fill_cell(ws, f"{col}{row}", "")

    # ==================== 第二页：Layout Data (Results) ====================

    # Belt Length (rows 110-111) — Effective drive length
    _fill_cell(ws, "J110", _fmt(bp.effective_length))
    _fill_cell(ws, "K111", _fmt(bp.length_tolerance))

    # Tensioner Data Results (rows 115-116)
    _fill_cell(ws, "I115", _fmt(tn.torque))
    # Belt Take-up / Arm Ratio (row 116)
    if _fmt(tn.arm_length) != "":
        _fill_cell(ws, "I116", _fmt(tn.arm_length))
    # Nominal Working Angle
    _fill_cell(ws, "U116", _fmt(tn.angle))

    # ==================== Tensioner Pulley Geometry (rows 121-124) ====================
    if tn.type == "Automatic":
        # Install row (121)
        _fill_cell(ws, "J121", _fmt(tn.angle))
        # Nominal Belt row (123)
        _fill_cell(ws, "J123", _fmt(tn.angle))
        _fill_cell(ws, "L123", _fmt(bp.effective_length))
        _fill_cell(ws, "N123", _fmt(tn.torque))

    # Design tension per rib (O111)
    if tn.design_tension is not None and bp.ribs is not None and bp.ribs > 0:
        _fill_cell(ws, "U111", round(tn.design_tension / bp.ribs, 2))

    # ==================== 保存 ====================
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    wb.close()

    filename = f"FEAD_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )
