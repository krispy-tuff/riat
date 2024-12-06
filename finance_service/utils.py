import logging
from fastapi import HTTPException, Security
import httpx
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from schemas import TransactionInfo

DATABASE_SERVICE_URL = "http://db_service:8000"
AUTH_SERVICE_URL = "http://auth_service:8001/auth/verify-token"

security = HTTPBearer()
logger = logging.getLogger(__name__)

async def get_current_user(authorization: HTTPAuthorizationCredentials = Security(security)):
    logger.info("Verifying token")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            AUTH_SERVICE_URL,
            headers={"Authorization": f"Bearer {authorization.credentials}"}
        )
        if response.status_code != 200:
            logger.error("Invalid token")
            raise HTTPException(status_code=401, detail="Invalid token")
        logger.info("Token verified successfully")
        return response.json()

async def get_user_balance(user_id: int):
    logger.info(f"Fetching balance for user {user_id}")
    async with httpx.AsyncClient() as client:
        user_response = await client.get(f"{DATABASE_SERVICE_URL}/users/?user_id={user_id}")
        if user_response.status_code != 200:
            logger.error(f"User {user_id} not found")
            raise HTTPException(status_code=user_response.status_code, detail="User not found")
        logger.info(f"Balance fetched for user {user_id}")
        return user_response.json()

async def update_user_balance(user_id: int, new_balance: float):
    logger.info(f"Updating balance for user {user_id} to {new_balance}")
    async with httpx.AsyncClient() as client:
        update_response = await client.patch(
            f"{DATABASE_SERVICE_URL}/users/update-balance",
            json={"user_id": user_id, "balance": new_balance}
        )
        if update_response.status_code != 200:
            logger.error(f"Failed to update balance for user {user_id}")
            raise HTTPException(status_code=update_response.status_code, detail="Failed to update balance")
        logger.info(f"Balance updated for user {user_id}")

async def add_transaction_history(transaction: TransactionInfo):
    logger.info(f"Adding transaction history for user {transaction.user_id}")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DATABASE_SERVICE_URL}/history/transaction",
            json={
                "user_id": transaction.user_id,
                "amount": transaction.amount,
                "type": transaction.type
            }
        )
        if response.status_code != 200:
            logger.error(f"Failed to add transaction history for user {transaction.user_id}")
            raise HTTPException(status_code=response.status_code, detail="Failed to add transaction history")
        logger.info(f"Transaction history added for user {transaction.user_id}")