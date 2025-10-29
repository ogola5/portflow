from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TruckTelemetry(BaseModel):
    truck_id: str = Field(..., description="Unique truck identifier")
    driver_name: Optional[str]
    latitude: float
    longitude: float
    speed: float
    engine_temp: float
    fuel_level: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
