import logging
from app.core.database import db
from pymongo.errors import PyMongoError
from datetime import datetime

logger = logging.getLogger("maintenance_service")

async def save_component(data: dict):
    """Insert a component record into MongoDB."""
    try:
        if "installation_date" not in data:
            data["installation_date"] = datetime.utcnow()
        result = await db["components"].insert_one(data)
        logger.info(f"Inserted component with _id: {result.inserted_id}")
        return result.inserted_id
    except PyMongoError as e:
        logger.error(f"Failed to insert component: {e}", exc_info=True)
        return None

async def log_breakdown(data: dict):
    """Insert a breakdown event into MongoDB."""
    try:
        if "timestamp" not in data:
            data["timestamp"] = datetime.utcnow()
        result = await db["breakdowns"].insert_one(data)
        logger.info(f"Inserted breakdown with _id: {result.inserted_id}")
        return result.inserted_id
    except PyMongoError as e:
        logger.error(f"Failed to insert breakdown: {e}", exc_info=True)
        return None

async def log_maintenance(data: dict):
    """Insert a maintenance log into MongoDB."""
    try:
        if "maintenance_date" not in data:
            data["maintenance_date"] = datetime.utcnow()
        result = await db["maintenance_logs"].insert_one(data)
        logger.info(f"Inserted maintenance log with _id: {result.inserted_id}")
        return result.inserted_id
    except PyMongoError as e:
        logger.error(f"Failed to insert maintenance log: {e}", exc_info=True)
        return None
