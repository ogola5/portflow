from app.core.database import db

async def save_container_event(data: dict):
    await db["container_events"].insert_one(data)

async def get_recent_container_events(limit: int = 10):
    cursor = db["container_events"].find().sort("timestamp", -1).limit(limit)
    return await cursor.to_list(length=limit)
