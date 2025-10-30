# app/core/database.py
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------------------
# MongoDB Client & DB
# ----------------------------
try:
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.DATABASE_NAME]
    logger.info(f"Connected to MongoDB database: {settings.DATABASE_NAME}")
except Exception as e:
    logger.error(f"Error connecting to MongoDB: {e}")
    raise

# ----------------------------
# Helper functions for persistence
# ----------------------------

async def insert_one(collection_name: str, document: dict):
    """Insert a single document and return inserted_id."""
    try:
        result = await db[collection_name].insert_one(document)
        logger.info(f"Document inserted into {collection_name} with ID: {result.inserted_id}")
        return result.inserted_id
    except Exception as e:
        logger.error(f"Failed to insert document into {collection_name}: {e}")
        raise

async def find(collection_name: str, query: dict = {}, limit: int = 0, sort: tuple = None):
    """Retrieve documents from a collection."""
    try:
        cursor = db[collection_name].find(query)
        if sort:
            cursor = cursor.sort(*sort)
        if limit > 0:
            cursor = cursor.limit(limit)
        results = await cursor.to_list(length=limit if limit > 0 else None)
        return results
    except Exception as e:
        logger.error(f"Failed to fetch documents from {collection_name}: {e}")
        raise
