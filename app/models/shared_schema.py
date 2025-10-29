# app/models/shared_schema.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import hashlib

class SharedBase(BaseModel):
    """Base schema for shared data correlation across agencies."""
    shared_id: str = Field(..., description="Unified data ID across all sources")
    source: str = Field(..., description="Source system (KRA, KPA, TRUCKER, CFS)")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @staticmethod
    def generate_shared_id(*args: str) -> str:
        """Generate a shared hash ID using source reference values."""
        concat = ":".join(args)
        return hashlib.sha256(concat.encode()).hexdigest()
