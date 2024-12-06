from pydantic import BaseModel

class DepositRequest(BaseModel):
    user_id: int
    amount: float

class BalanceResponse(BaseModel):
    user_id: int
    balance: float

class TransactionInfo(BaseModel):
    user_id: int
    amount: float
    type: str

class NotificationMessage(BaseModel):
    type: str
    user_id: int
    content: str