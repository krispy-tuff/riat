from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    balance: float


class Token(BaseModel):
    access_token: str
    token_type: str
