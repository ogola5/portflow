# app/models/kpa.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.shared_schema import SharedBase

class KPAData(SharedBase):
    vessel_name: str
    container_id: str
    operation_status: str
    berth_number: Optional[str]
    arrival_time: datetime
    departure_time: Optional[datetime]
