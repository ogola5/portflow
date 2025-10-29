# app/models/cfs.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.shared_schema import SharedBase


class CFSData(SharedBase):
    """Schema for Container Freight Station data."""
    cfs_name: str = Field(..., description="Name of the CFS (e.g., Consolbase, Mitchell Cotts)")
    container_number: str = Field(..., description="Unique container number (e.g., MSKU1234567)")
    kpa_transfer_order: str = Field(..., description="Official KPA transfer order number")
    delivery_order_number: Optional[str] = Field(None, description="Shipping line delivery order number")
    kra_release_confirmation: bool = Field(default=False, description="Whether KRA has cleared this container")
    storage_status: Optional[str] = Field("In Yard", description="Status: In Yard / Released / Awaiting Payment")
    cfs_charges_paid: bool = Field(default=False, description="Whether CFS storage/handling charges are paid")
    gate_pass_issued: bool = Field(default=False, description="Indicates whether gate pass has been issued for release")
    last_updated: datetime = Field(default_factory=datetime.utcnow)
