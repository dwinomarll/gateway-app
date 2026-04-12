import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from backend.notion import get_my4_notes, get_page, update_page

MOCK_PAGE = {"id": "abc-123", "properties": {"Accounts": {"title": [{"text": {"content": "Test Merchant"}}]}}}
MOCK_QUERY_RESPONSE = {"results": [MOCK_PAGE], "has_more": False, "next_cursor": None}

@pytest.mark.asyncio
async def test_get_my4_notes_returns_list():
    with patch("backend.notion.httpx.AsyncClient") as mock_class:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCK_QUERY_RESPONSE
        mock_response.raise_for_status = MagicMock()
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_class.return_value = mock_client
        result = await get_my4_notes()
    assert isinstance(result, list)
    assert result[0]["id"] == "abc-123"

@pytest.mark.asyncio
async def test_get_page_returns_page_dict():
    with patch("backend.notion.httpx.AsyncClient") as mock_class:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_response = MagicMock()
        mock_response.json.return_value = MOCK_PAGE
        mock_response.raise_for_status = MagicMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_class.return_value = mock_client
        result = await get_page("abc-123")
    assert result["id"] == "abc-123"

@pytest.mark.asyncio
async def test_update_page_sends_patch():
    with patch("backend.notion.httpx.AsyncClient") as mock_class:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_response = MagicMock()
        mock_response.json.return_value = MOCK_PAGE
        mock_response.raise_for_status = MagicMock()
        mock_client.patch = AsyncMock(return_value=mock_response)
        mock_class.return_value = mock_client
        result = await update_page("abc-123", {"Status": {"select": {"name": "Closed"}}})
    mock_client.patch.assert_called_once()
    assert "abc-123" in mock_client.patch.call_args[0][0]
