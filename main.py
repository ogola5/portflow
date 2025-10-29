from fastapi import FastAPI
from app.api import router as api_router

app = FastAPI(title="PortFlow Backend")

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "PortFlow backend is running!"}
