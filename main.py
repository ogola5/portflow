from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router as api_router
from app.services.scheduler_service import maintenance_reminder_loop
import asyncio

app = FastAPI(title="PortFlow Maintenance API")

# --- CORS: allow any URL ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",                # local dev
        "https://your-frontend-prod.com",       
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Startup tasks ---
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(maintenance_reminder_loop())

# --- API router ---
app.include_router(api_router, prefix="/api/v1")

# --- Root endpoint ---
@app.get("/")
async def root():
    
    return {"message": "PortFlow backend is running successfully!"}
