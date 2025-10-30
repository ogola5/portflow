# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.api import router as api_router
# from app.services.scheduler_service import maintenance_reminder_loop
# import asyncio

# app = FastAPI(title="PortFlow Maintenance API")

# # --- CORS: allow any URL ---
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:3000",                # local dev
#         "https://portflow-6m7v.onrender.com",       
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # --- Startup tasks ---
# @app.on_event("startup")
# async def startup_event():
#     asyncio.create_task(maintenance_reminder_loop())

# # --- API router ---
# app.include_router(api_router, prefix="/api/v1")

# # --- Root endpoint ---
# @app.get("/")
# async def root():
    
#     return {"message": "PortFlow backend is running successfully!"}

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api import router as api_router
from app.services.scheduler_service import maintenance_reminder_loop
import asyncio
import logging

# --- Configure logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("portflow")

app = FastAPI(title="PortFlow Maintenance API")

# --- CORS middleware ---
origins = [
    "http://localhost:3000",                # local dev
    "https://portflow-6m7v.onrender.com",  # frontend deployed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Global exception handler ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

# --- Startup tasks ---
@app.on_event("startup")
async def startup_event():
    try:
        asyncio.create_task(maintenance_reminder_loop())
        logger.info("Maintenance reminder loop started successfully.")
    except Exception as e:
        logger.error(f"Failed to start maintenance loop: {e}", exc_info=True)

# --- API router ---
app.include_router(api_router, prefix="/api/v1")

# --- Root endpoint ---
@app.get("/")
async def root():
    return {"message": "PortFlow backend is running successfully!"}