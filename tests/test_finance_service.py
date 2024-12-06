import pytest
from httpx import AsyncClient

BASE_URL = "http://localhost:8003/finance"
TEST_USER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIn0.DLXMS8JeC50jAe5_yB0TRRpAsX13IZ5NnhMTTiQ3cPY"  # Предполагается, что у вас есть тестовый токен пользователя

@pytest.mark.asyncio
async def test_deposit_funds():
    async with AsyncClient() as client:
        headers = {"Authorization": f"Bearer {TEST_USER_TOKEN}"}
        response = await client.post(f"{BASE_URL}/deposit", params={"amount": 100.0}, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert "balance" in data
        assert data["balance"] >= 100.0

@pytest.mark.asyncio
async def test_get_balance():
    async with AsyncClient() as client:
        headers = {"Authorization": f"Bearer {TEST_USER_TOKEN}"}
        response = await client.get(f"{BASE_URL}/balance", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert "balance" in data



@pytest.mark.asyncio
async def test_deposit_negative_amount():
    async with AsyncClient() as client:
        headers = {"Authorization": f"Bearer {TEST_USER_TOKEN}"}
        response = await client.post(f"{BASE_URL}/deposit", params={"amount": -100.0}, headers=headers)
        assert response.status_code == 400
        assert response.json()["detail"] == "Deposit amount must be positive"

@pytest.mark.asyncio
async def test_withdraw_insufficient_balance():
    async with AsyncClient() as client:
        headers = {"Authorization": f"Bearer {TEST_USER_TOKEN}"}
        response = await client.post(f"{BASE_URL}/withdraw", params={"amount": 1000000.0}, headers=headers)
        assert response.status_code == 400
        assert response.json()["detail"] == "Insufficient balance"