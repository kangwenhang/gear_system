from fastapi import FastAPI
from app.api.belts import router as belts_router
from app.api.calculate import router as calculate_router

app = FastAPI(title="Gear System API")

app.include_router(belts_router, prefix="/api", tags=["Belts"])
app.include_router(calculate_router, prefix="/api", tags=["Calculate"])

@app.get("/")
def read_root():
    return {"message": "Gear System API is running"}