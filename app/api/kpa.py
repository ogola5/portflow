from fastapi import APIRouter
from app.models.kpa import KPAData
from app.core.database import db

router = APIRouter(prefix="/kpa", tags=["KPA Data"])

@router.post("/ingest")
async def ingest_kpa_data(payload: KPAData):
    await db["kpa_data"].insert_one(payload.model_dump())
    return {"message": "KPA data ingested successfully", "shared_id": payload.shared_id}
