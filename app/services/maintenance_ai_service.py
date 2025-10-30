# app/services/maintenance_ai_service.py
from app.core.database import db
from datetime import datetime
import httpx
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

async def analyze_maintenance_needs():
    """Analyze trucks and suggest maintenance tasks via Gemini."""
    telemetry_data = await db["truck_telemetry"].find().sort("timestamp", -1).to_list(100)
    if not telemetry_data:
        return {"status": "no data"}

    # Prepare the context for Gemini
    input_text = "Analyze the following truck data and recommend maintenance routines:\n"
    for t in telemetry_data:
        input_text += f"Truck {t['truck_id']} speed={t['speed']} temp={t['engine_temp']} fuel={t['fuel_level']}\n"

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            headers={"Content-Type": "application/json"},
            params={"key": GEMINI_API_KEY},
            json={"contents": [{"parts": [{"text": input_text}]}]},
        )

    gemini_response = response.json()
    suggestions = gemini_response.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

    # Log suggestions
    await db["maintenance_suggestions"].insert_one({
        "generated_at": datetime.utcnow(),
        "analysis": suggestions
    })

    return {"message": "AI maintenance analysis complete", "suggestions": suggestions}
