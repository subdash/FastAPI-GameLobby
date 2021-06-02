import pytest
from datetime import datetime
from httpx import AsyncClient
from starlette import status

from src.main import app

ENDPOINT = "http://127.0.0.1/availability"


@pytest.mark.asyncio
async def test_post_root_response_is_200():
    async with AsyncClient(app=app, base_url=ENDPOINT) as ac:
        response = await ac.post("/", json={
            "user_id": 1,
            "time_avail": str(datetime.now()),
        })

    assert response.status_code == 200
    assert response.headers['content-type'] == "application/json"
    assert "time_avail" in response.json().keys()
    assert isinstance(response.json()['time_avail'], str)

    try:
        datetime.fromisoformat(response.json()['time_avail'])
    except ValueError:
        raise status.HTTP_422_UNPROCESSABLE_ENTITY
