# app/models/truck.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TruckTelemetry(BaseModel):
    truck_id: str = Field(..., description="Unique truck identifier")
    driver_name: Optional[str]
    latitude: float
    longitude: float
    speed: float
    engine_temp: float
    fuel_level: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
