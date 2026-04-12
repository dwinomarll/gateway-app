import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from backend.chat import proxy_chat

MOCK_RESPONSE = {"id": "chatcmpl-abc", "choices": [{"message": {"role": "assistant", "content": "Hello paps"}}]}

@pytest.mark.asyncio
async def test_proxy_chat_returns_completions_response():
    with patch("backend.chat.httpx.AsyncClient") as mock_class:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_response = MagicMock()
        mock_response.json.return_value = MOCK_RESPONSE
        mock_response.raise_for_status = MagicMock()
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_class.return_value = mock_client
        result = await proxy_chat({"messages": [{"role": "user", "content": "hello"}]})
    assert "choices" in result
    assert result["choices"][0]["message"]["content"] == "Hello paps"

@pytest.mark.asyncio
async def test_proxy_chat_sends_bearer_token():
    with patch("backend.chat.httpx.AsyncClient") as mock_class:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_response = MagicMock()
        mock_response.json.return_value = MOCK_RESPONSE
        mock_response.raise_for_status = MagicMock()
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_class.return_value = mock_client
        with patch("backend.chat.get_openclaw_token", return_value="test-token"):
            await proxy_chat({"messages": []})
    headers = mock_client.post.call_args[1]["headers"]
    assert headers["Authorization"] == "Bearer test-token"
