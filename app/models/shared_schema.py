# app/models/shared_schema.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import hashlib

class SharedBase(BaseModel):
    shared_id: str = Field(..., description="Unified data ID across all sources")
    source: str = Field(..., description="Source system (KRA, KPA, TRUCKER, CFS)")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @staticmethod
    def generate_shared_id(*args: str) -> str:
        concat = ":".join(args)
        return hashlib.sha256(concat.encode()).hexdigest()

class SharedIdentifiers(SharedBase):
    container_number: Optional[str]
    bill_of_lading: Optional[str]
    vessel_name: Optional[str]
    voyage_number: Optional[str]
