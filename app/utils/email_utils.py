import smtplib
import asyncio
from email.mime.text import MIMEText
from app.core.config import settings


async def send_email(to: str, subject: str, body: str):
    """Send email using credentials from .env (asynchronously)."""
    
    def _send_blocking():
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = settings.email_from
        msg["To"] = to

        with smtplib.SMTP(settings.email_host, settings.email_port) as server:
            server.starttls()
            server.login(settings.email_user, settings.email_password)
            server.send_message(msg)

    # Run blocking SMTP in thread to avoid blocking FastAPI loop
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _send_blocking)
