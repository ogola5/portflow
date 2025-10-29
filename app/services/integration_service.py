from app.core.database import db

async def get_unified_container_record(container_number: str):
    kpa = await db["kpa_data"].find_one({"container_number": container_number})
    kra = await db["kra_data"].find_one({"container_number": container_number})
    cfs = await db["cfs_data"].find_one({"container_number": container_number})
    truck = await db["truck_data"].find_one({"container_number": container_number})
    
    unified = {
        "container_number": container_number,
        "kpa": kpa,
        "kra": kra,
        "cfs": cfs,
        "truck": truck
    }
    return unified
