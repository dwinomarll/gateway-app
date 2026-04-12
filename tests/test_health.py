import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import httpx
from backend.health import check_service, get_health

@pytest.mark.asyncio
async def test_check_service_returns_ok_on_200():
    mock_response = MagicMock()
    mock_response.status_code = 200
    with patch("backend.health.httpx.AsyncClient") as mock_class:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_class.return_value = mock_client
        result = await check_service("http://test", method="GET")
    assert result == "ok"

@pytest.mark.asyncio
async def test_check_service_returns_down_on_connect_error():
    with patch("backend.health.httpx.AsyncClient") as mock_class:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.get = AsyncMock(side_effect=httpx.ConnectError("refused"))
        mock_class.return_value = mock_client
        result = await check_service("http://test", method="GET")
    assert result == "down"

@pytest.mark.asyncio
async def test_check_service_returns_down_on_timeout():
    with patch("backend.health.httpx.AsyncClient") as mock_class:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.get = AsyncMock(side_effect=httpx.TimeoutException("timeout"))
        mock_class.return_value = mock_client
        result = await check_service("http://test", method="GET")
    assert result == "down"

@pytest.mark.asyncio
async def test_get_health_returns_all_three_keys():
    with patch("backend.health.check_service", new_callable=AsyncMock, return_value="ok"):
        result = await get_health()
    assert set(result.keys()) == {"openclaw", "n8n", "shift4"}
    assert all(v in ("ok", "degraded", "down") for v in result.values())

@pytest.mark.asyncio
async def test_get_health_reflects_individual_status():
    async def mock_check(url, method="GET"):
        if "18790" in url: return "ok"
        if "n8n" in url: return "down"
        return "degraded"
    with patch("backend.health.check_service", side_effect=mock_check):
        result = await get_health()
    assert result["openclaw"] == "ok"
    assert result["n8n"] == "down"
    assert result["shift4"] == "degraded"
