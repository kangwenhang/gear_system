import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.belts import router as belts_router
from app.api.calculate import router as calculate_router

app = FastAPI(title="Gear System API")

app.include_router(belts_router, prefix="/api", tags=["Belts"])
app.include_router(calculate_router, prefix="/api", tags=["Calculate"])

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend_dist"

if FRONTEND_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIR / "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        requested_file = FRONTEND_DIR / full_path
        if requested_file.is_file():
            return FileResponse(str(requested_file))
        index_file = FRONTEND_DIR / "index.html"
        if index_file.is_file():
            return FileResponse(str(index_file))
        return {"message": "Gear System API is running"}
else:
    @app.get("/")
    def read_root():
        return {"message": "Gear System API is running"}