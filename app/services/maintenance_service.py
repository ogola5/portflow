from app.core.database import db

async def save_component(data: dict):
    await db["components"].insert_one(data)

async def log_breakdown(data: dict):
    await db["breakdowns"].insert_one(data)

async def log_maintenance(data: dict):
    await db["maintenance_logs"].insert_one(data)
