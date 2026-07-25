from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

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