import re
import uuid

def generate_ticket_id() -> str:
    return f"TICK-{uuid.uuid4().hex[:6].upper()}"

def generate_payment_id() -> str:
    return f"PAY-{uuid.uuid4().hex[:8].upper()}"

def sanitize_channel_name(name: str) -> str:
    clean = re.sub(r'[^a-zA-Z0-9\-]', '', name.lower().replace(" ", "-"))
    return clean[:30] or "ticket"

def format_currency(amount: float) -> str:
    return f"${amount:,.2f}"
  
