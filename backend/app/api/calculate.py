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