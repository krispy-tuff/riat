from pydantic import BaseModel
from datetime import datetime

class GameHistoryResponse(BaseModel):
    user_id: int
    game: str
    bet_amount: float
    win_amount: float
    timestamp: datetime

class TransactionHistoryResponse(BaseModel):
    amount: float
    type: str
    timestamp: datetime


class UserStatsResponse(BaseModel):
    user_id: int
    username: str
    total_balance: float
    total_games_played: int
    total_win_amount: float
