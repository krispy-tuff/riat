import pytest
from httpx import AsyncClient

BASE_URL = "http://localhost:8004/reports"
TEST_USER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIn0.DLXMS8JeC50jAe5_yB0TRRpAsX13IZ5NnhMTTiQ3cPY"  # Тестовый токен пользователя

@pytest.mark.asyncio
async def test_get_user_stats_success():
    async with AsyncClient() as client:
        headers = {"Authorization": f"Bearer {TEST_USER_TOKEN}"}
        response = await client.get(f"{BASE_URL}/user-stats", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert "username" in data
        assert "total_balance" in data
        assert "total_games_played" in data
        assert "total_win_amount" in data


@pytest.mark.asyncio
async def test_get_user_stats_invalid_token():
    async with AsyncClient() as client:
        headers = {"Authorization": "Bearer invalid_token"}
        response = await client.get(f"{BASE_URL}/user-stats", headers=headers)
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid token"


@pytest.mark.asyncio
async def test_get_user_game_history_success():
    async with AsyncClient() as client:
        headers = {"Authorization": f"Bearer {TEST_USER_TOKEN}"}
        response = await client.get(f"{BASE_URL}/user-game-history", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if data:  # Если есть данные в истории
            assert "user_id" in data[0]
            assert "game" in data[0]
            assert "bet_amount" in data[0]
            assert "win_amount" in data[0]
            assert "timestamp" in data[0]


@pytest.mark.asyncio
async def test_get_user_game_history_no_history():
    async with AsyncClient() as client:
        headers = {"Authorization": f"Bearer {TEST_USER_TOKEN}"}
        response = await client.get(f"{BASE_URL}/user-game-history", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)  # Даже при отсутствии истории должен возвращаться пустой список


@pytest.mark.asyncio
async def test_get_user_transaction_history_success():
    async with AsyncClient() as client:
        headers = {"Authorization": f"Bearer {TEST_USER_TOKEN}"}
        response = await client.get(f"{BASE_URL}/user-transaction-history", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if data:  # Если есть данные в истории
            assert "amount" in data[0]
            assert "type" in data[0]
            assert "timestamp" in data[0]


@pytest.mark.asyncio
async def test_get_user_transaction_history_no_history():
    async with AsyncClient() as client:
        headers = {"Authorization": f"Bearer {TEST_USER_TOKEN}"}
        response = await client.get(f"{BASE_URL}/user-transaction-history", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)  # Даже при отсутствии истории должен возвращаться пустой список
