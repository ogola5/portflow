# app/models/kra.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.shared_schema import SharedBase

class KRAData(SharedBase):
    """Schema for customs and taxation data (KRA)."""
    customs_entry_number: str = Field(..., description="KRA declaration entry number (e.g., C7)")
    hs_code: str = Field(..., description="Harmonized System code for goods classification")
    consignee_pin: str = Field(..., description="Importer KRA PIN")
    customs_value: float = Field(..., description="Declared CIF value of goods")
    taxes_paid: bool = Field(default=False, description="Whether customs taxes have been cleared")
    invoice_number: Optional[str] = Field(None, description="Commercial invoice number")
    permit_number: Optional[str] = Field(None, description="KEBS/KEPHIS/other regulatory permit number")
    kra_release_time: Optional[datetime] = Field(None, description="Timestamp of final KRA clearance")
