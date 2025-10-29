# app/services/truck_service.py
from app.core.database import db
from bson import ObjectId

def serialize_doc(doc):
    """Convert MongoDB document (ObjectId → str) to JSON-serializable format."""
    if not doc:
        return {}
    doc["_id"] = str(doc["_id"]) if "_id" in doc else None
    return doc

async def save_truck_telemetry(data: dict):
    """Persist truck telemetry data into MongoDB."""
    await db["truck_telemetry"].insert_one(data)

async def get_recent_truck_data(limit: int = 10):
    """Retrieve recent truck telemetry data, sorted by timestamp."""
    cursor = db["truck_telemetry"].find().sort("timestamp", -1).limit(limit)
    docs = await cursor.to_list(length=limit)
    return [serialize_doc(doc) for doc in docs]
