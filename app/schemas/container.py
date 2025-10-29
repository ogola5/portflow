from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ContainerEvent(BaseModel):
    container_id: str = Field(..., description="Unique container code")
    location: str
    status: str  # e.g., "arrived", "loaded", "cleared"
    kra_ref: Optional[str]
    cfs_name: Optional[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
