import asyncio, httpx
from backend.config import OPENCLAW_URL, N8N_URL, SHIFT4_STATUS_URL

async def check_service(url: str, method: str = "GET") -> str:
    try:
        async with httpx.AsyncClient() as client:
            if method == "HEAD":
                r = await client.head(url, timeout=5)
            else:
                r = await client.get(url, timeout=5)
            if r.status_code < 400: return "ok"
            elif r.status_code < 500: return "degraded"
            else: return "down"
    except (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError):
        return "down"
    except Exception:
        return "down"

async def get_health() -> dict:
    openclaw, n8n, shift4 = await asyncio.gather(
        check_service(f"{OPENCLAW_URL}/health"),
        check_service(N8N_URL, method="HEAD"),
        check_service(SHIFT4_STATUS_URL),
    )
    return {"openclaw": openclaw, "n8n": n8n, "shift4": shift4}
