# app/api/truckers.py
from fastapi import APIRouter
from app.models.truck import TruckTelemetry
from app.services.truck_service import save_truck_telemetry, get_recent_truck_data

router = APIRouter()

@router.post("/ingest")
async def ingest_truck_data(payload: TruckTelemetry):
    await save_truck_telemetry(payload.dict())
    return {"message": "Truck telemetry ingested successfully"}

@router.get("/recent")
async def get_recent(limit: int = 10):
    data = await get_recent_truck_data(limit)
    return {"count": len(data), "data": data}
