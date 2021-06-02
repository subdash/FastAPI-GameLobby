import pytest
from httpx import AsyncClient

from src.main import app

ENDPOINT = "http://127.0.0.1/games"


@pytest.mark.asyncio
async def test_get_root():
    async with AsyncClient(app=app, base_url=ENDPOINT) as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    # E.g. {'name': 'Settlers of Catan', 'min_players': 2, 'max_players': 4}
    first_obj = response.json()[0]
    assert {"name", "min_players", "max_players"} == set(first_obj.keys())
    assert isinstance(first_obj["name"], str)
    assert isinstance(first_obj["min_players"], int)
    assert isinstance(first_obj["max_players"], int)


@pytest.mark.asyncio
async def test_get_root_limit():
    async with AsyncClient(app=app, base_url=ENDPOINT) as ac:
        response = await ac.get("/?limit=1")

    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
