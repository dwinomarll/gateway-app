import httpx
from backend.config import OPENCLAW_URL, get_openclaw_token

async def proxy_chat(message: dict) -> dict:
    token = get_openclaw_token()
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{OPENCLAW_URL}/v1/chat/completions",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=message, timeout=60)
        r.raise_for_status()
        return r.json()
