from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = models.User(
        username=user.username,
        hashed_password=user.hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@users_router.get("/", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@users_router.get("/by-username/", response_model=schemas.UserOut)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@users_router.patch("/update-balance", response_model=schemas.UserOut)
def update_balance(data: schemas.UserUpdateBalance, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.balance = data.balance
    db.commit()
    db.refresh(user)
    return user

history_router = APIRouter(
    prefix="/history",
    tags=["History"]
)
@history_router.get("/games/", response_model=list[schemas.GameHistoryResponse])
def get_game_history(user_id: int, db: Session = Depends(get_db)):
    history = db.query(models.GameHistory).filter(models.GameHistory.user_id == user_id).all()
    if not history:
        raise HTTPException(status_code=404, detail="Game history not found")
    return history


@history_router.get("/transactions/", response_model=list[schemas.TransactionHistoryResponse])
def get_transaction_history(user_id: int, db: Session = Depends(get_db)):
    history = db.query(models.TransactionHistory).filter(models.TransactionHistory.user_id == user_id).all()
    if not history:
        raise HTTPException(status_code=404, detail="Transaction history not found")
    return history

@history_router.post("/game", response_model=schemas.GameResult)
def add_game_history(data: schemas.GameResult, db: Session = Depends(get_db)):
    new_game = models.GameHistory(
        user_id=data.user_id,
        game=data.game,
        bet_amount=data.bet_amount,
        win_amount=data.win_amount,
    )
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game

@history_router.post("/transaction", response_model=schemas.TransactionInfo)
def add_transaction_history(data: schemas.TransactionInfo, db: Session = Depends(get_db)):
    new_transaction = models.TransactionHistory(
        user_id=data.user_id,
        amount=data.amount,
        type=data.type,
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction