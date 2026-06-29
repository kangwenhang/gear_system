import json
from pathlib import Path
from fastapi import APIRouter

router = APIRouter()

PULLEY_PATH = Path(__file__).parent.parent / "data" / "pulleys.json"
MANUFACTURER_PATH = Path(__file__).parent.parent / "data" / "belt.json"

@router.get("/belt-options")
def get_belt_options():
    with open(PULLEY_PATH, "r", encoding="utf-8") as f:
        pulleys = json.load(f)
    return {"belt_options": pulleys}

@router.get("/manufacturer-options")
def get_manufacturer_options():
    with open(MANUFACTURER_PATH, "r", encoding="utf-8") as f:
        manufacturers = json.load(f)
    return {"manufacturers": manufacturers}