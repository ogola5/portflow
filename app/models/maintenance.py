from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.core.database import db


# ----------------------------
#  Pydantic Schemas
# ----------------------------

class Component(BaseModel):
    component_id: str = Field(..., description="Unique identifier for the component")
    name: str
    category: str
    manufacturer: Optional[str] = None
    installation_date: datetime = Field(default_factory=datetime.utcnow)
    expected_lifespan_hours: int = Field(..., description="Expected lifespan in operational hours")


class BreakdownEvent(BaseModel):
    component_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    issue_description: str
    downtime_hours: float
    repaired_by: Optional[str] = None
    part_used: Optional[str] = None


class MaintenanceLog(BaseModel):
    component_id: str
    maintenance_date: datetime = Field(default_factory=datetime.utcnow)
    performed_by: str
    notes: Optional[str] = None
    status: str = Field(default="completed", description="Status of the maintenance")
    next_due_date: Optional[datetime] = None


class MaintenanceRoutine(BaseModel):
    component_id: str
    frequency_days: int = Field(..., description="How often maintenance should occur")
    last_maintenance_date: datetime = Field(default_factory=datetime.utcnow)
    next_due_date: datetime = Field(default_factory=datetime.utcnow)


# ----------------------------
#  Async Persistence Functions
# ----------------------------

async def save_component(component: Component):
    await db["components"].insert_one(component.model_dump())


async def log_breakdown(event: BreakdownEvent):
    await db["breakdowns"].insert_one(event.model_dump())


async def log_maintenance(log: MaintenanceLog):
    await db["maintenance_logs"].insert_one(log.model_dump())


async def save_routine(routine: MaintenanceRoutine):
    await db["maintenance_routines"].insert_one(routine.model_dump())
