from fastapi import  HTTPException,  Security
import httpx
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from schemas import GameResult

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


async def get_user_balance(user_id: int):
    """
    Получает баланс пользователя из сервиса базы данных.
    """
    async with httpx.AsyncClient() as client:
        user_response = await client.get(f"{DATABASE_SERVICE_URL}/users/?user_id={user_id}")
        if user_response.status_code != 200:
            raise HTTPException(status_code=user_response.status_code, detail="User not found")
        return user_response.json()


async def update_user_balance(user_id: int, new_balance: float):
    """
    Обновляет баланс пользователя в сервисе базы данных.
    """
    async with httpx.AsyncClient() as client:
        update_response = await client.patch(
            f"{DATABASE_SERVICE_URL}/users/update-balance",
            json={"user_id": user_id, "balance": new_balance}
        )
        if update_response.status_code != 200:
            raise HTTPException(status_code=update_response.status_code, detail="Failed to update balance")

async def add_game_history(game: GameResult):
    """
    Добавляет запись об игре в историю.
    """
    async with httpx.AsyncClient() as client:
        history_response = await client.post(
            f"{DATABASE_SERVICE_URL}/history/game",
            json={"user_id": game.user_id, "game": game.game, "bet_amount": game.bet_amount, "win_amount": game.win_amount}
        )
        if history_response.status_code != 200:
            raise HTTPException(status_code=history_response.status_code, detail="Failed to add game history")