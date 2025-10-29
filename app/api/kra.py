from fastapi import APIRouter, HTTPException
from app.models.kra import KRAData
from app.core.database import db

router = APIRouter(prefix="/kra", tags=["KRA Data"])

@router.post("/ingest")
async def ingest_kra_data(payload: KRAData):
    await db["kra_data"].insert_one(payload.model_dump())
    return {"message": "KRA data ingested successfully", "shared_id": payload.shared_id}
