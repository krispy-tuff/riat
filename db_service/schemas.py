from datetime import datetime

from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    hashed_password: str

class UserUpdateBalance(BaseModel):
    user_id: int
    balance: float

class UserOut(BaseModel):
    id: int
    username: str
    balance: float
    hashed_password: str


class GameResult(BaseModel):
    user_id: int
    game: str
    bet_amount: float
    win_amount: float

class GameHistoryResponse(BaseModel):
    user_id: int
    game: str
    bet_amount: float
    win_amount: float
    timestamp: datetime


class TransactionInfo(BaseModel):
    user_id: int
    amount: float
    type: str

class TransactionHistoryResponse(BaseModel):
    user_id: int
    amount: float
    type: str
    timestamp: datetime



class UserStatsResponse(BaseModel):
    user_id: int
    username: str
    total_balance: float
    total_games_played: int
    total_wins: float
