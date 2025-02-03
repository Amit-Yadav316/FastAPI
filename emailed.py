import os
from aiosmtplib import send
from email.message import EmailMessage


SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

SMTP_USERNAME = os.getenv("SMTP_USERNAME", "yadavineet9198@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "myor bvsk yicv msdw")


async def send_email(to_email: str, subject: str, body: str):
    msg = EmailMessage()
    msg["From"] = SMTP_USERNAME
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    await send(
        msg,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        username=SMTP_USERNAME,
        password=SMTP_PASSWORD,
        start_tls=True,
    )
