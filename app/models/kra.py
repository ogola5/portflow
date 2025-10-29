# app/models/kra.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.shared_schema import SharedBase

class KRAData(SharedBase):
    kra_reference: str = Field(..., description="KRA customs reference number")
    consignment_value: float
    importer_name: str
    tax_status: str
    clearance_date: datetime = Field(default_factory=datetime.utcnow)
