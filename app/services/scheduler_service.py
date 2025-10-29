import asyncio
from datetime import datetime, timedelta
from app.core.database import db
from app.utils.email_utils import send_email

CHECK_INTERVAL = 60 * 60 * 24  # check once every 24h

async def maintenance_reminder_loop():
    """Background task to send reminders for upcoming maintenance."""
    while True:
        now = datetime.utcnow()
        upcoming = await db["maintenance_routines"].find(
            {"next_due_date": {"$lte": now + timedelta(days=3)}}
        ).to_list(None)

        for item in upcoming:
            component = await db["components"].find_one({"component_id": item["component_id"]})
            if component:
                await send_email(
                    to="maintenance_team@portflow.ai",
                    subject=f"Maintenance Due Soon: {component['name']}",
                    body=(
                        f"Component {component['name']} (ID: {component['component_id']}) "
                        f"is due for maintenance on {item['next_due_date']}.\n\n"
                        "Please confirm spare part availability and schedule work."
                    ),
                )

        await asyncio.sleep(CHECK_INTERVAL)
