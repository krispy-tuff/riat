import logging
from fastapi import APIRouter, HTTPException, Depends
from schemas import GameResult, GameResultResponse
from game_logic import play_slots, play_roulette
from utils import get_current_user, update_user_balance, get_user_balance, add_game_history

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/games", tags=["Games"])


@router.post("/roulette", response_model=GameResultResponse)
async def play_roulette_endpoint(bet_amount: float, chosen_color: str, user: dict = Depends(get_current_user)):
    """
    Эндпоинт для игры в рулетку. Пользователь делает ставку на цвет (red, black, green).
    """
    logger.info(f"User {user['user_id']} is playing roulette with bet amount {bet_amount} on color {chosen_color}")
    if chosen_color not in ["red", "black", "green"]:
        logger.warning(f"Invalid color choice by user {user['user_id']}: {chosen_color}")
        raise HTTPException(status_code=400, detail="Invalid color choice. Choose red, black, or green.")

    user_id = user["user_id"]
    user_data = await get_user_balance(user_id)

    if user_data["balance"] < bet_amount:
        logger.warning(f"User {user_id} has insufficient balance for bet amount {bet_amount}")
        raise HTTPException(status_code=400, detail="Insufficient balance")

    win_amount, result_color = play_roulette(bet_amount, chosen_color)
    new_balance = user_data["balance"] - bet_amount + win_amount

    await update_user_balance(user_id, new_balance)
    game = GameResult(user_id=user_id, game="roulette", bet_amount=bet_amount, win_amount=win_amount)
    await add_game_history(game)

    logger.info(f"User {user_id} played roulette and won {win_amount}, new balance is {new_balance}")
    return {"user_id": user_id, "game": "roulette", "bet_amount": bet_amount, "win_amount": win_amount,
            "result": result_color}


@router.post("/slots", response_model=GameResultResponse)
async def play_slots_endpoint(bet_amount: float, user: dict = Depends(get_current_user)):
    """
    Эндпоинт для игры в слоты. Пользователь делает ставку и получает выигрыш в зависимости от выпавших символов.
    """
    logger.info(f"User {user['user_id']} is playing slots with bet amount {bet_amount}")
    user_id = user["user_id"]
    user_data = await get_user_balance(user_id)

    if user_data["balance"] < bet_amount:
        logger.warning(f"User {user_id} has insufficient balance for bet amount {bet_amount}")
        raise HTTPException(status_code=400, detail="Insufficient balance")

    win_amount, symbols = play_slots(bet_amount)
    new_balance = user_data["balance"] - bet_amount + win_amount

    await update_user_balance(user_id, new_balance)
    game = GameResult(user_id=user_id, game="slots", bet_amount=bet_amount, win_amount=win_amount)
    await add_game_history(game)

    logger.info(f"User {user_id} played slots and won {win_amount}, new balance is {new_balance}")
    return {"user_id": user_id, "game": "slots", "bet_amount": bet_amount, "win_amount": win_amount,
            "result": symbols}
