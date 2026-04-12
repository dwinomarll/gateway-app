import httpx
import logging
from backend.config import get_notion_token, NOTION_BASE_URL, NOTION_API_VERSION, MY4_NOTES_DB

log = logging.getLogger(__name__)


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {get_notion_token()}",
        "Notion-Version": NOTION_API_VERSION,
        "Content-Type": "application/json",
    }


async def get_my4_notes() -> list[dict]:
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{NOTION_BASE_URL}/databases/{MY4_NOTES_DB}/query",
            headers=_headers(),
            json={
                "sorts": [{"property": "Next Follow-up", "direction": "ascending"}],
                "filter": {"property": "Task Status", "status": {"does_not_equal": "Done"}},
                "page_size": 50,
            },
            timeout=10,
        )
        r.raise_for_status()
        data = r.json()
        results = data.get("results", [])
        if data.get("has_more"):
            log.warning("get_my4_notes: has_more=True, results truncated at %d", len(results))
        return results


async def get_page(page_id: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{NOTION_BASE_URL}/pages/{page_id}",
            headers=_headers(),
            timeout=10,
        )
        r.raise_for_status()
        return r.json()


async def update_page(page_id: str, properties: dict) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.patch(
            f"{NOTION_BASE_URL}/pages/{page_id}",
            headers=_headers(),
            json={"properties": properties},
            timeout=10,
        )
        r.raise_for_status()
        return r.json()
