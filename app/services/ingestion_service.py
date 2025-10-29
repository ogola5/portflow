from app.models.truck import save_truck_telemetry
from app.models.container import save_container_event

async def process_truck_data(payload: dict):
    # Here you can normalize / clean fields
    # Example: convert engine temp from Fahrenheit to Celsius
    if "engine_temp" in payload:
        payload["engine_temp"] = round((payload["engine_temp"] - 32) * 5/9, 2)
    await save_truck_telemetry(payload)
    return {"message": "Truck data ingested successfully"}

async def process_container_data(payload: dict):
    await save_container_event(payload)
    return {"message": "Container event recorded successfully"}
