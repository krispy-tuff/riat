from pydantic import BaseModel

class GameResult(BaseModel):
    user_id: int
    game: str
    bet_amount: float
    win_amount: float

class GameResultResponse(BaseModel):
    user_id: int
    game: str
    bet_amount: float
    win_amount: float
    result: str | list[str]
