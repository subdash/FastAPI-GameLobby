import random
import pytest
from httpx import AsyncClient

from src.main import app

ENDPOINT = "http://127.0.0.1/users"


@pytest.mark.asyncio
async def test_get_root():
    async with AsyncClient(app=app, base_url="http://127.0.0.1/token") as ac:
        token_response = await ac.post("/", data={
            "username": "dash",
            "password": "password"
        })

    access_token = token_response.json()['access_token']
    header = {'authorization': f"Bearer {access_token}"}

    async with AsyncClient(app=app, base_url=ENDPOINT) as ac:
        response = await ac.get("/", headers=header)

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    first_obj = response.json()[0]
    assert {'username', 'email', 'availability', 'interest', 'disabled'} == \
           set(first_obj.keys())

    assert isinstance(first_obj["username"], str)
    assert isinstance(first_obj["email"], str)
    assert isinstance(first_obj["availability"], list)
    assert isinstance(first_obj["interest"], list)

    # Substitute for type check of `Optional[bool]`
    try:
        assert isinstance(first_obj["disabled"], bool)
    except AssertionError:
        assert first_obj["disabled"] is None


@pytest.mark.asyncio
async def test_get_root_limit_401():
    async with AsyncClient(app=app, base_url=ENDPOINT) as ac:
        response = await ac.get("/?limit=1")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_root_limit():
    async with AsyncClient(app=app, base_url="http://127.0.0.1/token") as ac:
        token_response = await ac.post("/", data={
            "username": "dash",
            "password": "password"
        })

    access_token = token_response.json()['access_token']
    header = {'authorization': f"Bearer {access_token}"}

    async with AsyncClient(app=app, base_url=ENDPOINT) as ac:
        response = await ac.get("/?limit=1", headers=header)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_post_root():
    async with AsyncClient(app=app, base_url=ENDPOINT) as ac:
        rand_int = random.randint(100, 999)
        response = await ac.post("/", json={
            "username": f"d{rand_int}",
            "email": f"ds{rand_int}@s.com",
            "password": "password"
        })

    assert response.status_code == 200
    assert response.url == "http://127.0.0.1/"


@pytest.mark.asyncio
async def test_post_root_400_existing_user():
    async with AsyncClient(app=app, base_url=ENDPOINT) as ac:
        rand_int = random.randint(100, 999)
        response = await ac.post("/", json={
            "username": "dash",
            "email": f"ds{rand_int}@s.com",
            "password": "password"
        })

    assert response.status_code == 400
    assert response.url == ENDPOINT + "/"


@pytest.mark.asyncio
async def test_post_root_400_existing_email():
    async with AsyncClient(app=app, base_url=ENDPOINT) as ac:
        rand_int = random.randint(100, 999)
        response = await ac.post("/", json={
            "username": f"dash{rand_int}",
            "email": f"ds@sd.com",
            "password": "password"
        })

    assert response.status_code == 400
    assert response.url == ENDPOINT + "/"


@pytest.mark.asyncio
async def test_get_detail_401():
    async with AsyncClient(app=app, base_url=ENDPOINT) as ac:
        response = await ac.get("/1/")

    assert response.status_code == 401
    assert "detail" in response.json().keys()
    assert response.json()['detail'] == "Not authenticated"


@pytest.mark.asyncio
async def test_get_detail_200():
    async with AsyncClient(app=app, base_url="http://127.0.0.1/token") as ac:
        token_response = await ac.post("/", data={
            "username": "dash",
            "password": "password"
        })

    access_token = token_response.json()['access_token']
    header = {'authorization': f"Bearer {access_token}"}

    async with AsyncClient(app=app, base_url=ENDPOINT) as ac:
        detail_response = await ac.get("/1/", headers=header)

    assert detail_response.status_code == 200
    assert {'username', 'email', 'availability', 'interest', 'disabled'} == \
           set(detail_response.json().keys())
    assert isinstance(detail_response.json()["username"], str)
    assert isinstance(detail_response.json()["email"], str)
    assert isinstance(detail_response.json()["availability"], list)
    assert isinstance(detail_response.json()["interest"], list)

    # Substitute for type check of `Optional[bool]`
    try:
        assert isinstance(detail_response.json()["disabled"], bool)
    except AssertionError:
        assert detail_response.json()["disabled"] is None
