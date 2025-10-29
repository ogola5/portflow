from fastapi import APIRouter, HTTPException
from app.schemas.truck import TruckTelemetry
from app.schemas.container import ContainerEvent
from app.services.ingestion_service import (
    process_truck_data,
    process_container_data
)

router = APIRouter(prefix="/ingest", tags=["Ingestion"])

@router.post("/truck")
async def ingest_truck_data(truck_data: TruckTelemetry):
    try:
        result = await process_truck_data(truck_data.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/container")
async def ingest_container_data(container_data: ContainerEvent):
    try:
        result = await process_container_data(container_data.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
