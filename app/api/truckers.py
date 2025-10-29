from fastapi import APIRouter
from app.models.truck import TruckTelemetry, save_truck_telemetry

router = APIRouter(prefix="/truckers", tags=["Truckers"])

@router.post("/ingest")
async def ingest_trucker_data(payload: TruckTelemetry):
    await save_truck_telemetry(payload.model_dump())
    return {"message": "Truck telemetry ingested", "shared_id": payload.shared_id}
