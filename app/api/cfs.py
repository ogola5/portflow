from fastapi import APIRouter
from app.models.cfs import CFSData
from app.core.database import db

router = APIRouter(prefix="/cfs", tags=["CFS Data"])

@router.post("/ingest")
async def ingest_cfs_data(payload: CFSData):
    await db["cfs_data"].insert_one(payload.model_dump())
    return {"message": "CFS data ingested successfully", "shared_id": payload.shared_id}
