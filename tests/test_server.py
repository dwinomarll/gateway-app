import pytest
from unittest.mock import patch, AsyncMock
from httpx import AsyncClient, ASGITransport

MOCK_HEALTH = {"openclaw": "ok", "n8n": "ok", "shift4": "ok"}
MOCK_CASES = [{"id": "abc", "properties": {}}]
MOCK_PAGE = {"id": "abc", "properties": {}}
MOCK_CHAT = {"choices": [{"message": {"role": "assistant", "content": "Hi"}}]}
VALID_UUID = "12345678-1234-5678-1234-567812345678"

@pytest.fixture
def app():
    from backend.server import app
    return app

@pytest.mark.asyncio
async def test_health_endpoint(app):
    with patch("backend.server.get_health", new_callable=AsyncMock, return_value=MOCK_HEALTH):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            r = await ac.get("/health")
    assert r.status_code == 200
    assert set(r.json().keys()) == {"openclaw", "n8n", "shift4"}

@pytest.mark.asyncio
async def test_notion_feed(app):
    with patch("backend.server.get_my4_notes", new_callable=AsyncMock, return_value=MOCK_CASES):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            r = await ac.get("/notion")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

@pytest.mark.asyncio
async def test_notion_page(app):
    with patch("backend.server.get_page", new_callable=AsyncMock, return_value=MOCK_PAGE):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            r = await ac.get(f"/notion/{VALID_UUID}")
    assert r.status_code == 200

@pytest.mark.asyncio
async def test_notion_patch(app):
    with patch("backend.server.update_page", new_callable=AsyncMock, return_value=MOCK_PAGE) as mock_update:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            r = await ac.patch(f"/notion/{VALID_UUID}", json={"Status": {"select": {"name": "Closed"}}})
    assert r.status_code == 200
    mock_update.assert_called_once_with(VALID_UUID, {"Status": {"select": {"name": "Closed"}}})

@pytest.mark.asyncio
async def test_chat_endpoint(app):
    with patch("backend.server.proxy_chat", new_callable=AsyncMock, return_value=MOCK_CHAT):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            r = await ac.post("/chat", json={"messages": [{"role": "user", "content": "hello"}]})
    assert r.status_code == 200
    assert "choices" in r.json()
