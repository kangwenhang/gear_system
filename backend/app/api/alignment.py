from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()


class PulleyInput(BaseModel):
    name: str
    code: str
    x: Optional[float] = None
    y: Optional[float] = None
    flat_dia: Optional[float] = None
    groove_dia: Optional[float] = None
    type: str
    inertia: Optional[float] = None
    service_factor: Optional[float] = None


class AlignmentInput(BaseModel):
    pulleys: List[PulleyInput]
    center_height: float = 0.0
    perpendicularity: float = 0.0


class AlignmentPairResult(BaseModel):
    pulley_from: str
    pulley_to: str
    contact_exit: Optional[float] = None
    contact_entry: Optional[float] = None
    wrap_angle: Optional[float] = None
    check: Optional[float] = None
    center_height_diff: Optional[float] = None
    perpendicularity: Optional[float] = None
    tilt_direction: Optional[float] = None
    camber_entry: Optional[float] = None
    camber_exit: Optional[float] = None
    toe_entry: Optional[float] = None
    toe_exit: Optional[float] = None
    bea_groove_groove: Optional[float] = None
    twist_groove_groove: Optional[float] = None
    offset_groove_groove: Optional[float] = None
    bea_groove_flat: Optional[float] = None
    twist_groove_flat: Optional[float] = None


@router.post("/alignment/calculate")
def calculate_alignment(req: AlignmentInput):
    """
    计算对齐度
    
    输入参数：
    - pulleys: 带轮列表（来自轮系布局页）
    - center_height: 中心高 (mm)
    - perpendicularity: 垂直度 (mm/m)
    
    输出：各相邻带轮对的对齐度参数
    """
    results = []
    
    valid_pulleys = [p for p in req.pulleys if p.x is not None and p.y is not None]
    
    for i in range(len(valid_pulleys)):
        p1 = valid_pulleys[i]
        p2 = valid_pulleys[(i + 1) % len(valid_pulleys)]
        
        d1 = p1.flat_dia if p1.type == "flat" else p1.groove_dia
        d2 = p2.flat_dia if p2.type == "flat" else p2.groove_dia
        
        if d1 is None or d2 is None:
            continue
        
        # ======== 预留：计算公式位置 ========
        # TODO: 待用户提供公式后实现计算逻辑
        # 目前返回占位值
        
        result = AlignmentPairResult(
            pulley_from=p1.code or p1.name or f"轮{i+1}",
            pulley_to=p2.code or p2.name or f"轮{(i+1) % len(valid_pulleys) + 1}",
            contact_exit=None,
            contact_entry=None,
            wrap_angle=None,
            check=None,
            center_height_diff=req.center_height,
            perpendicularity=req.perpendicularity,
            tilt_direction=None,
            camber_entry=0.0,
            camber_exit=0.0,
            toe_entry=0.0,
            toe_exit=0.0,
            bea_groove_groove=None,
            twist_groove_groove=0.0,
            offset_groove_groove=0.0,
            bea_groove_flat=None,
            twist_groove_flat=0.0,
        )
        
        results.append(result)
    
    return {
        "success": True,
        "count": len(results),
        "results": results
    }
