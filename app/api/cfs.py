# app/api/cfs.py
from fastapi import APIRouter
from app.models.cfs import CFSData

router = APIRouter()

@router.post("/ingest")
def ingest_cfs_data(record: CFSData):
    return {"message": "CFS data ingested successfully", "record": record}
