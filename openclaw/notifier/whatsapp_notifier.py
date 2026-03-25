import os
from twilio.rest import Client

def send_whatsapp_alert(job: dict) -> str:
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("WHATSAPP_FROM")
    to_number = os.getenv("WHATSAPP_TO")

    if not all([account_sid, auth_token, from_number, to_number]):
        raise RuntimeError("Missing Twilio WhatsApp environment variables")

    client = Client(account_sid, auth_token)

    body = (
        f"🚀 New job found!\n\n"
        f"Title: {job.get('title', 'N/A')}\n"
        f"Company: {job.get('company', 'N/A')}\n"
        f"Location: {job.get('location', 'N/A')}\n"
        f"Link: {job.get('url', 'N/A')}"
    )

    message = client.messages.create(
        from_=from_number,
        to=to_number,
        body=body,
    )

    return message.sid
