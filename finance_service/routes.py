import logging
from fastapi import APIRouter, HTTPException, Depends

from schemas import BalanceResponse, NotificationMessage, TransactionInfo
from rabbitmq_utils import publish_message
from utils import get_current_user, update_user_balance, get_user_balance, add_transaction_history

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/finance", tags=["Finance"])

@router.post("/deposit", response_model=BalanceResponse)
async def deposit_funds(amount: float, user: dict = Depends(get_current_user)):
    """
    Эндпоинт для внесения средств на счет пользователя.
    """
    logger.info(f"User {user['user_id']} is depositing {amount}")
    user_id = user["user_id"]

    if amount <= 0:
        logger.warning(f"User {user_id} attempted to deposit a non-positive amount: {amount}")
        raise HTTPException(status_code=400, detail="Deposit amount must be positive")

    user_data = await get_user_balance(user_id)
    new_balance = user_data["balance"] + amount
    await update_user_balance(user_id, new_balance)

    message = NotificationMessage(
        type="balance_update",
        user_id=user_id,
        content=f"Your account has been credited with ${amount:.2f}."
    )
    publish_message(dict(message))
    transaction = TransactionInfo(user_id=user_id, amount=amount, type="deposit")
    await add_transaction_history(transaction)

    logger.info(f"User {user_id} deposited {amount}, new balance is {new_balance}")
    return {"user_id": user_id, "balance": new_balance}

@router.get("/balance", response_model=BalanceResponse)
async def get_balance(user: dict = Depends(get_current_user)):
    """
    Эндпоинт для получения текущего баланса пользователя.
    """
    logger.info(f"User {user['user_id']} is requesting balance")
    user_id = user["user_id"]
    user_data = await get_user_balance(user_id)
    logger.info(f"User {user_id} balance is {user_data['balance']}")
    return {"user_id": user_id, "balance": user_data["balance"]}

@router.post("/withdraw", response_model=BalanceResponse)
async def withdraw_funds(amount: float, user: dict = Depends(get_current_user)):
    """
    Эндпоинт для снятия средств со счета пользователя.
    """
    logger.info(f"User {user['user_id']} is withdrawing {amount}")
    user_id = user["user_id"]

    if amount <= 0:
        logger.warning(f"User {user_id} attempted to withdraw a non-positive amount: {amount}")
        raise HTTPException(status_code=400, detail="Withdrawal amount must be positive")

    user_data = await get_user_balance(user_id)

    if user_data["balance"] < amount:
        logger.warning(f"User {user_id} has insufficient balance for withdrawal: {amount}")
        raise HTTPException(status_code=400, detail="Insufficient balance")

    new_balance = user_data["balance"] - amount
    await update_user_balance(user_id, new_balance)

    message = NotificationMessage(
        type="balance_update",
        user_id=user_id,
        content=f"You have successfully withdrawn ${amount:.2f}."
    )
    publish_message(dict(message))

    transaction = TransactionInfo(user_id=user_id, amount=amount, type="withdrawal")
    await add_transaction_history(transaction)

    logger.info(f"User {user_id} withdrew {amount}, new balance is {new_balance}")
    return {"user_id": user_id, "balance": new_balance}