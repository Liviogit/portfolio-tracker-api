from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.user_model import User
from services.auth_service import get_current_user
from database import get_db
from services.trade_service import (
    create_trade, get_trades, update_trade, delete_trade, get_trades_by_portfolio
)
from serializers.trade_serializer import TradeCreate, TradeRead

trade_router = APIRouter(prefix="/trades", tags=["trades"])


@trade_router.post("/", response_model=TradeRead)
def create_trade_endpoint(trade: TradeCreate, db: Session = Depends(get_db)):
    return create_trade(db, trade)


@trade_router.get("/", response_model=list[TradeRead])
def read_trades(db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    return get_trades(db,current_user.user_id)


@trade_router.get("/portfolio/{portfolio_id}", response_model=list[TradeRead])
def read_trades_by_portfolio(portfolio_id: int,db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    return get_trades_by_portfolio(db,current_user.user_id, portfolio_id)