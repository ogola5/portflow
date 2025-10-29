from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SharedIdentifiers(BaseModel):
    container_number: str = Field(..., description="Unique container ID like MSKU1234567")
    bill_of_lading: Optional[str]
    vessel_name: Optional[str]
    voyage_number: Optional[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
