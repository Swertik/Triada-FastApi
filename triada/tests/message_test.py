import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch, call, ANY
from triada.handlers.message import handle_message
from fastapi.responses import PlainTextResponse
import asyncio
import httpx
from triada.config.settings import JUDGE_CHAT_ID


@pytest_asyncio.fixture
async def mock_vk_client():
    mock_response = AsyncMock()
    mock_response.json.return_value = {"response": 1234567}
    
    mock_client = AsyncMock()
    mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
    
    return mock_client

@pytest.mark.asyncio
async def message_test(message: dict, called: bool = True, mock_vk_client = None):
    if not mock_vk_client:
        mock_response = AsyncMock()
        mock_response.json.return_value = {"response": 1234567}
        
        mock_vk_client = AsyncMock()
        mock_vk_client.__aenter__.return_value.post.return_value = mock_response

    with patch('httpx.AsyncClient', return_value=mock_vk_client):
        response = await handle_message(message)

    if called:
        mock_vk_client.__aenter__.return_value.post.assert_called()
        call_args = mock_vk_client.__aenter__.return_value.post.call_args_list
        return call_args
    else:
        mock_vk_client.__aenter__.return_value.post.assert_not_called()
        return response

@pytest.mark.asyncio
async def test_message_proccess(mock_vk_client):
    hello_calls = await message_test({'text': '.привет', 
                                    'peer_id': JUDGE_CHAT_ID,
                                    'from_id': 123456}, called=True, mock_vk_client=mock_vk_client)
    assert hello_calls == [call('https://api.vk.com/method/messages.send', params={'access_token': ANY, 'peer_id': 2000000002, 'message': 'Привет!', 'random_id': ANY, 'v': '5.199', 'attachment': []})]


if __name__ == "__main__":
    print(asyncio.run(message_test({'text': '.привет', 
                                    'peer_id': JUDGE_CHAT_ID,
                                    'from_id': 123456}, called=True)))

