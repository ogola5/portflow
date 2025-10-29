from fastapi import APIRouter, HTTPException
from app.models.kpa import KPARecord
from app.core.database import db

router = APIRouter(prefix="/kpa", tags=["KPA"])

@router.post("/ingest")
async def ingest_kpa_data(payload: KPARecord):
    existing = await db["kpa_data"].find_one({"container_number": payload.container_number})
    if existing:
        await db["kpa_data"].update_one(
            {"container_number": payload.container_number},
            {"$set": payload.dict(exclude_unset=True)}
        )
        return {"message": "KPA record updated", "container_number": payload.container_number}
    await db["kpa_data"].insert_one(payload.dict())
    return {"message": "KPA record created", "container_number": payload.container_number}
