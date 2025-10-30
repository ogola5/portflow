from fastapi import APIRouter
from app.models.maintenance import (
    Component,
    BreakdownEvent,
    MaintenanceLog,
    MaintenanceRoutine,
    save_component,
    log_breakdown,
    log_maintenance,
    save_routine,
)
from app.core.database import db  # Needed for read endpoints
from app.utils.email_utils import send_email
router = APIRouter()
from app.services.maintenance_ai_service import analyze_maintenance_needs

router = APIRouter(prefix="/maintenance", tags=["Maintenance AI"])

# ----------------------------
#  CREATE / INGEST ENDPOINTS
# ----------------------------

@router.post("/component")
async def add_component(component: Component):
    """Add a new component record."""
    await save_component(component)
    return {"status": "success", "message": "Component saved successfully"}


@router.post("/breakdown")
async def add_breakdown(event: BreakdownEvent):
    """Log a breakdown event for a component."""
    await log_breakdown(event)
    return {"status": "success", "message": "Breakdown logged successfully"}


@router.post("/maintenance")
async def add_maintenance(log: MaintenanceLog):
    """Add a maintenance record."""
    await log_maintenance(log)
    return {"status": "success", "message": "Maintenance log recorded successfully"}


@router.post("/routine")
async def create_routine(routine: MaintenanceRoutine):
    """Define a maintenance routine for a component."""
    await save_routine(routine)
    return {"status": "success", "message": "Maintenance routine saved"}

@router.post("/test-email")
async def test_email(to: str):
    await send_email(
        to=to,
        subject="Test Maintenance Notification",
        body="This is a test message from PortFlow maintenance alert system."
    )
    return {"status": "Email sent", "to": to}

@router.get("/analyze")
async def run_maintenance_ai():
    """Run AI-based maintenance analysis using Gemini."""
    result = await analyze_maintenance_needs()
    return result
# ----------------------------
#  READ ENDPOINTS
# ----------------------------

@router.get("/components")
async def list_components():
    components = await db["components"].find().to_list(100)
    return components


@router.get("/breakdowns")
async def list_breakdowns():
    breakdowns = await db["breakdowns"].find().to_list(100)
    return breakdowns


@router.get("/logs")
async def list_maintenance_logs():
    logs = await db["maintenance_logs"].find().to_list(100)
    return logs


@router.get("/routines")
async def list_routines():
    routines = await db["maintenance_routines"].find().to_list(100)
    return routines
