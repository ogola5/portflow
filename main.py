from fastapi import FastAPI
from app.api import router as api_router
from app.services.scheduler_service import maintenance_reminder_loop
import asyncio

app = FastAPI(title="PortFlow Maintenance API")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(maintenance_reminder_loop())

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "PortFlow backend is running successfully!"}
