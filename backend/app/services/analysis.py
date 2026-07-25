# ✅ 如果你希望在 services 里写计算逻辑，可以在这里加
# 比如：齿轮系统分析、振动分析等

class GearCalculationService:
    @staticmethod
    async def calculate(pulleys: list):
        # 模拟计算：返回带轮数量和类型统计
        total = len(pulleys)
        groove_count = sum(1 for p in pulleys if p.get("type") == "groove")
        flat_count = total - groove_count
        
        return {
            "total_pulleys": total,
            "groove_pulleys": groove_count,
            "flat_pulleys": flat_count,
            "status": "analyzed"
        }