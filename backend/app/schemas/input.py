from pydantic import BaseModel
from typing import List, Optional

# 带轮选项
class BeltOption(BaseModel):
    code: str
    name: str

class BeltOptionsResponse(BaseModel):
    belt_options: List[BeltOption]

# ✅ 新增：前端表格数据结构（对应 InputPage.vue 里的 tableData）
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

class CalculationRequest(BaseModel):
    pulleys: List[PulleyInput]