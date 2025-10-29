# app/models/truck.py
from app.core.database import db
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.shared_schema import SharedBase

class TruckTelemetry(SharedBase):
    truck_id: str = Field(..., description="Unique truck identifier")
    driver_name: Optional[str]
    latitude: float
    longitude: float
    speed: float
    engine_temp: float
    fuel_level: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

async def save_truck_telemetry(data: dict):
    await db["truck_telemetry"].insert_one(data)

async def get_recent_truck_data(limit: int = 10):
    cursor = db["truck_telemetry"].find().sort("timestamp", -1).limit(limit)
    return await cursor.to_list(length=limit)
