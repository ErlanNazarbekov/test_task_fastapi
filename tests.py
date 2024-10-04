# -*- coding: utf-8 -*-
import pytest
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.schemas.kitten import KittenCreate, KittenDB, KittenUpdate
from app.schemas.breed import BreedCreate, BreedDB
from app.core.db import get_async_session

TOKEN = ""


@pytest.mark.asyncio
async def test_create_breed():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/breeds/",
            json={"name": "Сиамская"},
            headers={"Authorization": f"Bearer {TOKEN}"},
        )
    assert response.status_code == 200
    assert response.json()["name"] == "Сиамская"


@pytest.mark.asyncio
async def test_get_all_breeds():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(
            "/breeds/",
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_kitten():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        breed_response = await client.post(
            "/breeds/",
            json={"name": "Персидская"},
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        breed_id = breed_response.json()["id"]

        response = await client.post(
            "/kittens/",
            json={
                "name": "Пушок",
                "age": 3,
                "color": "белый",
                "description": "пушистый котенок",
                "breed_id": breed_id,
            },
            headers={"Authorization": f"Bearer {TOKEN}"}
        )

    assert response.status_code == 200
    assert response.json()["name"] == "Пушок"
    assert response.json()["breed_id"] == breed_id


@pytest.mark.asyncio
async def test_get_kittens():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(
            "/kittens/",
            headers={"Authorization": f"Bearer {TOKEN}"}
        )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_kitten_by_id():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        breed_response = await client.post(
            "/breeds/",
            json={"name": "Бенгальская"},
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        breed_id = breed_response.json()["id"]

        kitten_response = await client.post(
            "/kittens/",
            json={
                "name": "Лео",
                "age": 4,
                "color": "коричневый",
                "description": "храбрый котенок",
                "breed_id": breed_id,
            },
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        kitten_id = kitten_response.json()["id"]

        response = await client.get(
            f"/kittens/{kitten_id}",
            headers={"Authorization": f"Bearer {TOKEN}"}
        )

    assert response.status_code == 200
    assert response.json()["id"] == kitten_id
    assert response.json()["name"] == "Лео"


@pytest.mark.asyncio
async def test_get_kittens_by_breed():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        breed_response = await client.post(
            "/breeds/",
            json={"name": "Мейн-Кун"},
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        breed_id = breed_response.json()["id"]

        await client.post(
            "/kittens/",
            json={
                "name": "Маки",
                "age": 2,
                "color": "рыжий",
                "description": "будущий гигант",
                "breed_id": breed_id,
            },
            headers={"Authorization": f"Bearer {TOKEN}"}
        )

        # Получаем котят по породе
        response = await client.get(
            f"/kittens/breed/{breed_id}",
            headers={"Authorization": f"Bearer {TOKEN}"}
        )

    assert response.status_code == 200
    assert response.json()["breed_name"] == "Мейн-Кун"
    assert len(response.json()["kittens"]) > 0


@pytest.mark.asyncio
async def test_update_kitten():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        breed_response = await client.post(
            "/breeds/",
            json={"name": "Шотландская вислоухая"},
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        breed_id = breed_response.json()["id"]

        kitten_response = await client.post(
            "/kittens/",
            json={
                "name": "Мира",
                "age": 2,
                "color": "серый",
                "description": "спокойный котенок",
                "breed_id": breed_id,
            },
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        kitten_id = kitten_response.json()["id"]

        response = await client.patch(
            f"/kittens/{kitten_id}",
            json={
                "name": "Мира",
                "age": 3,
                "color": "серый",
                "description": "настоящая озорница",
                "breed_id": breed_id,
            },
            headers={"Authorization": f"Bearer {TOKEN}"}
        )

    assert response.status_code == 200
    assert response.json()["age"] == 3
    assert response.json()["description"] == "настоящая озорница"


@pytest.mark.asyncio
async def test_delete_kitten():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        breed_response = await client.post(
            "/breeds/",
            json={"name": "Сфинкс"},
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        breed_id = breed_response.json()["id"]

        kitten_response = await client.post(
            "/kittens/",
            json={
                "name": "Бибоп",
                "age": 1,
                "color": "розово-серый",
                "description": "игривый и ласковый",
                "breed_id": breed_id,
            },
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        kitten_id = kitten_response.json()["id"]

        response = await client.delete(
            f"/kittens/{kitten_id}",
            headers={"Authorization": f"Bearer {TOKEN}"}
        )

    assert response.status_code == 200
    assert response.json()["id"] == kitten_id
