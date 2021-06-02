import pytest
from httpx import AsyncClient

from src.main import app

ENDPOINT = "http://127.0.0.1/interest"


@pytest.mark.asyncio
async def test_post_root_response_is_200():
    async with AsyncClient(app=app, base_url=ENDPOINT) as ac:
        response = await ac.post("/", json={
            "user_id": 1,
            "game_id": 1,
        })

    assert response.status_code == 200
    assert response.headers['content-type'] == "application/json"
    assert {"user_id", "game_id"} == set(response.json().keys())
    assert isinstance(response.json()['user_id'], int)
    assert isinstance(response.json()['game_id'], int)
