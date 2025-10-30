from fastapi import APIRouter
from app.services.maintenance_ai_service import analyze_maintenance_needs

router = APIRouter(prefix="/maintenance", tags=["Maintenance AI"])

@router.get("/analyze")
async def run_maintenance_ai():
    """Run AI-based maintenance analysis using Gemini."""
    result = await analyze_maintenance_needs()
    return result
