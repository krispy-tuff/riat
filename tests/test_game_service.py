import pytest
from httpx import AsyncClient

BASE_URL = "http://localhost:8002/games"
TEST_USER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIn0.DLXMS8JeC50jAe5_yB0TRRpAsX13IZ5NnhMTTiQ3cPY"  # Тестовый токен пользователя

@pytest.mark.asyncio
async def test_play_roulette_success():
    async with AsyncClient() as client:
        headers = {"Authorization": f"Bearer {TEST_USER_TOKEN}"}
        response = await client.post(
            f"{BASE_URL}/roulette",
            params={"bet_amount": 10.0, "chosen_color": "red"},
            headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] is not None
        assert data["game"] == "roulette"
        assert "bet_amount" in data
        assert "win_amount" in data
        assert data["bet_amount"] == 10.0


@pytest.mark.asyncio
async def test_play_roulette_invalid_color():
    async with AsyncClient() as client:
        headers = {"Authorization": f"Bearer {TEST_USER_TOKEN}"}
        response = await client.post(
            f"{BASE_URL}/roulette",
            params={"bet_amount": 10.0, "chosen_color": "blue"},
            headers=headers
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid color choice. Choose red, black, or green."


@pytest.mark.asyncio
async def test_play_roulette_insufficient_balance():
    async with AsyncClient() as client:
        headers = {"Authorization": f"Bearer {TEST_USER_TOKEN}"}
        response = await client.post(
            f"{BASE_URL}/roulette",
            params={"bet_amount": 100000.0, "chosen_color": "red"},
            headers=headers
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Insufficient balance"


@pytest.mark.asyncio
async def test_play_slots_success():
    async with AsyncClient() as client:
        headers = {"Authorization": f"Bearer {TEST_USER_TOKEN}"}
        response = await client.post(
            f"{BASE_URL}/slots",
            params={"bet_amount": 10.0},
            headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] is not None
        assert data["game"] == "slots"
        assert "bet_amount" in data
        assert "win_amount" in data
        assert data["bet_amount"] == 10.0


@pytest.mark.asyncio
async def test_play_slots_insufficient_balance():
    async with AsyncClient() as client:
        headers = {"Authorization": f"Bearer {TEST_USER_TOKEN}"}
        response = await client.post(
            f"{BASE_URL}/slots",
            params={"bet_amount": 100000.0},
            headers=headers
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Insufficient balance"
