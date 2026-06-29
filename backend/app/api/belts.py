import json
from pathlib import Path
from fastapi import APIRouter

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


@router.get("/belt-options")
def get_belt_options():
    pulleys = load_pulleys()
    return {"belt_options": pulleys}


@router.get("/manufacturer-options")
def get_manufacturer_options():
    manufacturers = load_belts()
    return {"manufacturers": manufacturers}