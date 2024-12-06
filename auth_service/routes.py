import logging
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
import httpx
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import schemas, utils, jwt_handler

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])

DATABASE_SERVICE_URL = "http://db_service:8000"


@router.post("/register", response_model=schemas.UserOut)
async def register(user: Annotated[schemas.UserCreate, Depends()]):
    """
    Эндпоинт для регистрации нового пользователя.
    """
    logger.info(f"Registering user: {user.username}")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DATABASE_SERVICE_URL}/users/",
            json={
                "username": user.username,
                "hashed_password": utils.hash_password(user.password)
            }
        )
        if response.status_code != 200:
            logger.error(f"Failed to register user: {response.json()}")
            raise HTTPException(status_code=response.status_code, detail=response.json())
        logger.info(f"User registered successfully: {user.username}")
        return response.json()


@router.post("/login", response_model=schemas.Token)
async def login(user: Annotated[schemas.UserCreate, Depends()]):
    """
    Эндпоинт для входа пользователя в систему.
    """

    logger.info(f"User login attempt: {user.username}")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DATABASE_SERVICE_URL}/users/by-username/?username={user.username}")
        if response.status_code != 200:
            logger.warning(f"Invalid credentials for user: {user.username}")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        db_user = response.json()

        if not utils.verify_password(user.password, db_user["hashed_password"]):
            logger.warning(f"Invalid password for user: {user.username}")
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = jwt_handler.create_access_token({"sub": str(db_user["id"])})
        logger.info(f"User logged in successfully: {user.username}")
        return {"access_token": access_token, "token_type": "bearer"}


security = HTTPBearer()


@router.post("/verify-token")
def verify_token(token: HTTPAuthorizationCredentials = Depends(security)):
    """
    Эндпоинт для проверки токена пользователя.
    """
    logger.info("Verifying token")
    payload = jwt_handler.decode_access_token(token.credentials)
    user_id = payload.get("sub")
    if user_id is None:
        logger.error("Invalid token payload")
        raise HTTPException(status_code=401, detail="Invalid token payload")
    logger.info(f"Token verified successfully for user_id: {user_id}")
    return {"user_id": int(user_id)}
