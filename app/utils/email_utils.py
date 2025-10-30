# app/utils/email_utils.py
import smtplib
import asyncio
from email.mime.text import MIMEText
from app.core.config import settings


async def send_email(to: str, subject: str, body: str):
    """Send email asynchronously using SMTP credentials from .env."""

    def _send_blocking():
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = settings.EMAIL_FROM
        msg["To"] = to

        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
            server.send_message(msg)

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _send_blocking)
