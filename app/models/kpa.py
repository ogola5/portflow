from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.shared_schema import SharedIdentifiers

class KPARecord(SharedIdentifiers):
    terminal_of_discharge: Optional[str]
    gross_weight: Optional[float]
    cfs_nomination: Optional[str]
    free_days_expiry: Optional[datetime]
