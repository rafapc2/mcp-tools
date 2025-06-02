import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_read_item_valid_id_1():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["item_id"] == 1
    assert "Knife" in response.json()["name"]

@pytest.mark.asyncio
async def test_read_item_valid_id_2_with_query():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/items/2?q=test")
    assert response.status_code == 200
    assert response.json()["item_id"] == 2
    assert "Spoons" in response.json()["name"]

@pytest.mark.asyncio
async def test_read_item_invalid_id():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/items/99")
    assert response.status_code == 200
    assert response.json()["item_id"] == 99
    assert "fork" in response.json()["name"].lower()
