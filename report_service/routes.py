import logging
from fastapi import APIRouter, Depends
from schemas import UserStatsResponse, GameHistoryResponse, TransactionHistoryResponse
from utils import get_current_user, get_user_game_history, get_user_transaction_history, get_user_data

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reports", tags=["Reports"])

DATABASE_SERVICE_URL = "http://db_service:8000"

@router.get("/user-stats", response_model=UserStatsResponse)
async def get_user_stats(user: dict = Depends(get_current_user)):
    """
    Эндпоинт для получения статистики пользователя.
    """
    logger.info(f"Fetching user stats for user {user['user_id']}")
    user_id = user["user_id"]

    user_data = await get_user_data(user_id)
    games = await get_user_game_history(user_id)

    total_games_played = len(games)
    total_win_amount = sum(game["win_amount"] for game in games)

    logger.info(f"User stats fetched for user {user_id}")
    return {
        "user_id": user_id,
        "username": user_data["username"],
        "total_balance": user_data["balance"],
        "total_games_played": total_games_played,
        "total_win_amount": total_win_amount,
    }

@router.get("/user-game-history", response_model=list[GameHistoryResponse])
async def user_game_history(user: dict = Depends(get_current_user)):
    """
    Эндпоинт для получения истории игр пользователя.
    """
    logger.info(f"Fetching game history for user {user['user_id']}")
    user_id = user["user_id"]
    history = await get_user_game_history(user_id)
    logger.info(f"Game history fetched for user {user_id}")
    return history

@router.get("/user-transaction-history", response_model=list[TransactionHistoryResponse])
async def user_transaction_history(user: dict = Depends(get_current_user)):
    """
    Эндпоинт для получения истории транзакций пользователя.
    """
    logger.info(f"Fetching transaction history for user {user['user_id']}")
    user_id = user["user_id"]
    history = await get_user_transaction_history(user_id)
    logger.info(f"Transaction history fetched for user {user_id}")
    return history