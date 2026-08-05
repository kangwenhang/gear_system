from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

from app.services.gear_base import GearBaseService

router = APIRouter()

class PulleyItem(BaseModel):
    name: str
    code: str
    x: Optional[float] = None
    y: Optional[float] = None
    flat_dia: Optional[float] = None
    groove_dia: Optional[float] = None
    type: str
    inertia: Optional[float] = None
    service_factor: Optional[float] = Field(None, ge=1)

class CalculateRequest(BaseModel):
    info: dict
    pulleys: List[PulleyItem]


class BeltLengthRequest(BaseModel):
    """皮带长度计算请求"""
    pulleys: List[PulleyItem]
    belt_thickness: Optional[float] = 1.2    # Input!H21 带厚
    lining_thickness: Optional[float] = 1.0  # Input!H22 衬厚


class TensionerPositionRequest(BaseModel):
    """张紧轮坐标计算请求（基于短/长皮带长度）"""
    pulleys: List[PulleyItem]
    target_length: float
    tensioner_code: str = 'TEN'
    pivot_x: Optional[float] = None
    pivot_y: Optional[float] = None
    belt_thickness: Optional[float] = 1.2
    lining_thickness: Optional[float] = 1.0


class FreePositionRequest(BaseModel):
    """张紧器自由位置计算请求"""
    pulleys: List[PulleyItem]
    tensioner_code: str = 'TEN'
    pivot_x: Optional[float] = None
    pivot_y: Optional[float] = None
    nominal_angle: float = 25.0      # 名义扭转角
    rotation: str = 'cw'             # 旋转方向 cw/ccw
    belt_thickness: Optional[float] = 1.2
    lining_thickness: Optional[float] = 1.0


class InstallPositionRequest(BaseModel):
    """张紧器安装位置计算请求"""
    pulleys: List[PulleyItem]
    tensioner_code: str = 'TEN'
    pivot_x: Optional[float] = None
    pivot_y: Optional[float] = None
    stroke: float = 40.0             # 总行程(°)
    rotation: str = 'cw'             # 旋转方向 cw/ccw
    long_belt_length: Optional[float] = None  # 长皮带长度（用于判断安装困难）
    belt_thickness: Optional[float] = 1.2
    lining_thickness: Optional[float] = 1.0

@router.post("/calculate")
def calculate(req: CalculateRequest):
    try:
        results = []
        for p in req.pulleys:
            dia = (
                p.flat_dia
                if p.type == "flat" and p.flat_dia
                else p.groove_dia
            )
            if p.x is None or p.y is None or dia is None:
                continue
            radius = dia / 2
            results.append({
                "name": p.name,
                "x": p.x,
                "y": p.y,
                "radius_mm": round(radius, 2),
                "type": p.type
            })
        return {
            "success": True,
            "count": len(results),
            "pulleys": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/calc-belt-length")
def calc_belt_length(req: BeltLengthRequest):
    """
    计算皮带长度

    皮带总长 = Σ(切线段长度Q) + Σ(包角弧长)
             = Σ(C_i × cos(E_i)) + Σ(S_i × K_i × π / 360)

    其中:
    - C: 两带轮中心距
    - E: 上切点角（ASIN计算）
    - S: 包角（带轮上的皮带接触角）
    - K: 节圆直径
    """
    try:
        service = GearBaseService(
            belt_thickness=req.belt_thickness,
            lining_thickness=req.lining_thickness
        )
        pulleys_data = [p.model_dump() for p in req.pulleys]
        result = service.calc_belt_length(pulleys_data)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/calc-tensioner-position")
def calc_tensioner_position(req: TensionerPositionRequest):
    """
    计算短/长皮带长度对应的张紧轮XY坐标。
    张紧轮沿臂弧（以枢轴为圆心）搜索，使皮带长度 = 目标长度。
    """
    try:
        if req.pivot_x is None or req.pivot_y is None:
            raise HTTPException(status_code=400, detail="缺少枢轴坐标 pivot_x/pivot_y")
        service = GearBaseService(
            belt_thickness=req.belt_thickness,
            lining_thickness=req.lining_thickness
        )
        pulleys_data = [p.model_dump() for p in req.pulleys]
        result = service.calc_tensioner_position(
            pulleys=pulleys_data,
            target_length=req.target_length,
            tensioner_code=req.tensioner_code,
            pivot_x=req.pivot_x,
            pivot_y=req.pivot_y
        )
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return {"success": True, **result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/calc-free-position")
def calc_free_position(req: FreePositionRequest):
    """
    计算张紧器自由位置的皮带长度和张紧轮XY坐标。

    张紧器从自由位置旋转名义扭转角(nominal_angle)到达工作位置。
    旋转方向(cw/ccw)决定角度变化方向。
    """
    try:
        if req.pivot_x is None or req.pivot_y is None:
            raise HTTPException(status_code=400, detail="缺少枢轴坐标 pivot_x/pivot_y")
        service = GearBaseService(
            belt_thickness=req.belt_thickness,
            lining_thickness=req.lining_thickness
        )
        pulleys_data = [p.model_dump() for p in req.pulleys]
        result = service.calc_free_position(
            pulleys=pulleys_data,
            tensioner_code=req.tensioner_code,
            pivot_x=req.pivot_x,
            pivot_y=req.pivot_y,
            nominal_angle=req.nominal_angle,
            rotation=req.rotation
        )
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return {"success": True, **result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/calc-install-position")
def calc_install_position(req: InstallPositionRequest):
    """
    计算张紧器安装位置的皮带长度和张紧轮XY坐标。

    安装位置 = 工作位置反向旋转总行程(stroke)度（远离皮带方向）。
    安装困难判断：安装位置皮带长度 < 长皮带长度 → 提示安装困难。
    """
    try:
        if req.pivot_x is None or req.pivot_y is None:
            raise HTTPException(status_code=400, detail="缺少枢轴坐标 pivot_x/pivot_y")
        service = GearBaseService(
            belt_thickness=req.belt_thickness,
            lining_thickness=req.lining_thickness
        )
        pulleys_data = [p.model_dump() for p in req.pulleys]
        result = service.calc_install_position(
            pulleys=pulleys_data,
            tensioner_code=req.tensioner_code,
            pivot_x=req.pivot_x,
            pivot_y=req.pivot_y,
            stroke=req.stroke,
            rotation=req.rotation,
            long_belt_length=req.long_belt_length
        )
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return {"success": True, **result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))