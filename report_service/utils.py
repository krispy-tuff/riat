from fastapi import HTTPException, Security
import httpx
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

DATABASE_SERVICE_URL = "http://db_service:8000"
AUTH_SERVICE_URL = "http://auth_service:8001/auth/verify-token"

security = HTTPBearer()


async def get_current_user(authorization: HTTPAuthorizationCredentials = Security(security)):
    """
    Проверяет токен через сервис авторизации.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            AUTH_SERVICE_URL,
            headers={"Authorization": f"Bearer {authorization.credentials}"}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid token")
        return response.json()  # Возвращает {"user_id": user_id}


async def get_user_game_history(user_id: int):
    """
    Получает историю игр пользователя из базы данных.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DATABASE_SERVICE_URL}/history/games/?user_id={user_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Game history not found")
        return response.json()


async def get_user_transaction_history(user_id: int):
    """
    Получает историю транзакций пользователя из базы данных.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DATABASE_SERVICE_URL}/history/transactions/?user_id={user_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Transaction history not found")
        return response.json()

async def get_user_data(user_id: int):
    """
    Получает данные пользователя из базы данных.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DATABASE_SERVICE_URL}/users/?user_id={user_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="User not found")
        return response.json()