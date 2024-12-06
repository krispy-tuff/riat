from datetime import datetime, UTC

from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    balance = Column(Float, default=0.0)

class GameHistory(Base):
    __tablename__ = "game_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    game = Column(String, nullable=False)
    bet_amount = Column(Float, nullable=False)
    win_amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(UTC))

class TransactionHistory(Base):
    __tablename__ = "transaction_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # 'deposit' or 'withdraw'
    timestamp = Column(DateTime, default=datetime.now(UTC))
