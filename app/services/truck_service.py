# app/services/truck_service.py
from app.core.database import db

async def save_truck_telemetry(data: dict):
    """Persist truck telemetry data into MongoDB."""
    await db["truck_telemetry"].insert_one(data)

async def get_recent_truck_data(limit: int = 10):
    cursor = db["truck_telemetry"].find().sort("timestamp", -1).limit(limit)
    return await cursor.to_list(length=limit)
