import json
import csv
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse

router = APIRouter()

# 默认数据
DEFAULT_PULLEYS = [
    {"code": "CRK", "name": "曲轴"},
    {"code": "ALT", "name": "电机"},
    {"code": "AC", "name": "空调"},
    {"code": "IDR", "name": "惰轮"},
    {"code": "WP", "name": "水泵"},
    {"code": "FAN", "name": "风扇"},
    {"code": "TEN", "name": "张紧器"},
    {"code": "PS", "name": "助力转向泵"},
    {"code": "PUMP", "name": "泵"},
    {"code": "AIC", "name": "空气压缩机"}
]

DEFAULT_BELTS = [
    {"name": "Gates", "flat_to_pitch": 1.2, "pitch_to_effective": 1.0, "height": 4.4},
    {"name": "Roundus", "flat_to_pitch": 1.2, "pitch_to_effective": 1.2, "height": 4.7},
    {"name": "DAYCO", "flat_to_pitch": 1.2, "pitch_to_effective": 1.3, "height": 4.8},
    {"name": "BELT", "flat_to_pitch": 1.3, "pitch_to_effective": 1.5, "height": 5.3},
    {"name": "DaZhong", "flat_to_pitch": 1.5, "pitch_to_effective": 1.5, "height": 5.5},
    {"name": "GALUX", "flat_to_pitch": 1.2, "pitch_to_effective": 1.05, "height": 4.7},
    {"name": "YuJiang", "flat_to_pitch": 0.95, "pitch_to_effective": 1.15, "height": 4.3}
]


def get_data_dir():
    """获取数据目录，优先使用运行目录下的 data 文件夹"""
    # 优先使用运行目录（工作目录）下的 data 文件夹
    work_dir = Path.cwd()
    work_data_dir = work_dir / "data"
    
    # 如果运行目录有 data 目录，或者 data 目录不存在，就使用运行目录
    # 这样确保打包后能在运行目录创建数据文件
    if work_data_dir.exists() and work_data_dir.is_dir():
        return work_data_dir
    
    # 开发环境：使用脚本同级目录
    script_dir = Path(__file__).parent.parent / "data"
    if script_dir.exists() and script_dir.is_dir():
        # 如果脚本目录存在，但运行目录没有，就在运行目录创建
        if not work_data_dir.exists():
            work_data_dir.mkdir(parents=True, exist_ok=True)
        return work_data_dir
    
    # 都不存在时，在运行目录创建 data 目录
    work_data_dir.mkdir(parents=True, exist_ok=True)
    return work_data_dir


def ensure_data_file(filename, default_data):
    """确保数据文件存在，不存在则创建默认文件"""
    data_dir = get_data_dir()
    file_path = data_dir / filename
    
    if not file_path.exists():
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
    
    return file_path


def load_pulleys():
    """加载皮带轮数据"""
    file_path = ensure_data_file("pulleys.json", DEFAULT_PULLEYS)
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_belts():
    """加载皮带品牌数据"""
    file_path = ensure_data_file("belt.json", DEFAULT_BELTS)
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_pulleys(data: List[dict]):
    """保存皮带轮数据"""
    file_path = ensure_data_file("pulleys.json", DEFAULT_PULLEYS)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_belts(data: List[dict]):
    """保存皮带品牌数据"""
    file_path = ensure_data_file("belt.json", DEFAULT_BELTS)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@router.get("/belt-options")
def get_belt_options():
    pulleys = load_pulleys()
    return {"belt_options": pulleys}


@router.get("/manufacturer-options")
def get_manufacturer_options():
    manufacturers = load_belts()
    return {"manufacturers": manufacturers}


# ============ 导入导出功能 ============

@router.get("/export/pulleys")
def export_pulleys_csv():
    """导出皮带轮数据为 CSV 格式"""
    pulleys = load_pulleys()
    
    output = "code,name\n"
    for p in pulleys:
        output += f'{p.get("code", "")},{p.get("name", "")}\n'
    
    return StreamingResponse(
        iter([output]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=pulleys.csv"}
    )


@router.get("/export/belts")
def export_belts_csv():
    """导出皮带品牌数据为 CSV 格式"""
    belts = load_belts()
    
    output = "name,flat_to_pitch,pitch_to_effective,height\n"
    for b in belts:
        output += f'{b.get("name", "")},{b.get("flat_to_pitch", "")},{b.get("pitch_to_effective", "")},{b.get("height", "")}\n'
    
    return StreamingResponse(
        iter([output]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=belts.csv"}
    )


@router.post("/import/pulleys")
async def import_pulleys(file: UploadFile = File(...)):
    """导入皮带轮数据（支持 CSV 格式）
    
    CSV 格式要求：
    - 第一行为表头：code,name
    - 从第二行开始为数据
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="只支持 CSV 格式文件")
    
    content = await file.read()
    try:
        text = content.decode('utf-8')
        lines = text.strip().split('\n')
        
        if len(lines) < 2:
            raise HTTPException(status_code=400, detail="CSV 文件数据为空")
        
        # 解析 CSV（跳过表头）
        pulleys = []
        for line in lines[1:]:  # 跳过表头
            if not line.strip():
                continue
            parts = line.strip().split(',')
            if len(parts) >= 2:
                pulleys.append({
                    "code": parts[0].strip(),
                    "name": parts[1].strip()
                })
        
        if not pulleys:
            raise HTTPException(status_code=400, detail="未解析到有效数据")
        
        save_pulleys(pulleys)
        return {"message": f"成功导入 {len(pulleys)} 条皮带轮数据", "count": len(pulleys)}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"导入失败: {str(e)}")


@router.post("/import/belts")
async def import_belts(file: UploadFile = File(...)):
    """导入皮带品牌数据（支持 CSV 格式）
    
    CSV 格式要求：
    - 第一行为表头：name,flat_to_pitch,pitch_to_effective,height
    - 从第二行开始为数据
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="只支持 CSV 格式文件")
    
    content = await file.read()
    try:
        text = content.decode('utf-8')
        lines = text.strip().split('\n')
        
        if len(lines) < 2:
            raise HTTPException(status_code=400, detail="CSV 文件数据为空")
        
        # 解析 CSV（跳过表头）
        belts = []
        for line in lines[1:]:  # 跳过表头
            if not line.strip():
                continue
            parts = line.strip().split(',')
            if len(parts) >= 4:
                try:
                    belts.append({
                        "name": parts[0].strip(),
                        "flat_to_pitch": float(parts[1].strip()),
                        "pitch_to_effective": float(parts[2].strip()),
                        "height": float(parts[3].strip())
                    })
                except ValueError as e:
                    raise HTTPException(status_code=400, detail=f"数据类型错误: {line}")
        
        if not belts:
            raise HTTPException(status_code=400, detail="未解析到有效数据")
        
        save_belts(belts)
        return {"message": f"成功导入 {len(belts)} 条皮带品牌数据", "count": len(belts)}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"导入失败: {str(e)}")


# ============ 简单的 CRUD API ============

@router.put("/pulleys")
def update_pulleys(data: List[dict]):
    """更新所有皮带轮数据"""
    # 验证数据格式
    for p in data:
        if "code" not in p or "name" not in p:
            raise HTTPException(status_code=400, detail="每条数据必须包含 code 和 name")
    
    save_pulleys(data)
    return {"message": f"成功更新 {len(data)} 条皮带轮数据"}


@router.put("/belts")
def update_belts(data: List[dict]):
    """更新所有皮带品牌数据"""
    # 验证数据格式
    for b in data:
        required = ["name", "flat_to_pitch", "pitch_to_effective", "height"]
        for field in required:
            if field not in b:
                raise HTTPException(status_code=400, detail=f"每条数据必须包含 {field}")
            try:
                float(b[field])
            except (ValueError, TypeError):
                raise HTTPException(status_code=400, detail=f"{field} 必须是数字")
    
    save_belts(data)
    return {"message": f"成功更新 {len(data)} 条皮带品牌数据"}