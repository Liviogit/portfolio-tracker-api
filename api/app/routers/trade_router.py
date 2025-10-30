from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from services.trade_service import (
    create_trade, get_trades, get_trade, update_trade, delete_trade, get_trades_by_portfolio
)
from serializers.trade_serializer import TradeCreate, TradeRead

trade_router = APIRouter(prefix="/trades", tags=["trades"])


@trade_router.post("/", response_model=TradeRead)
def create_trade_endpoint(trade: TradeCreate, db: Session = Depends(get_db)):
    return create_trade(db, trade)


@trade_router.get("/", response_model=list[TradeRead])
def read_trades(db: Session = Depends(get_db)):
    return get_trades(db)


@trade_router.get("/portfolio/{portfolio_id}", response_model=list[TradeRead])
def read_trades_by_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    return get_trades_by_portfolio(db, portfolio_id)


@trade_router.get("/{trade_id}", response_model=TradeRead)
def read_trade(trade_id: int, db: Session = Depends(get_db)):
    trade = get_trade(db, trade_id)
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    return trade


@trade_router.put("/{trade_id}", response_model=TradeRead)
def update_trade_endpoint(trade_id: int, trade_update: TradeCreate, db: Session = Depends(get_db)):
    trade = update_trade(db, trade_id, trade_update)
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    return trade


@trade_router.delete("/{trade_id}", response_model=TradeRead)
def delete_trade_endpoint(trade_id: int, db: Session = Depends(get_db)):
    trade = delete_trade(db, trade_id)
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    return trade
