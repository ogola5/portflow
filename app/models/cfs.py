# app/models/cfs.py
from pydantic import BaseModel, Field
from datetime import datetime
from app.models.shared_schema import SharedBase

class CFSData(SharedBase):
    container_id: str
    location: str
    status: str
    stored_since: datetime = Field(default_factory=datetime.utcnow)
