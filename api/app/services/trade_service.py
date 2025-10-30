from sqlalchemy.orm import Session
from models.trade_model import Trade
from serializers.trade_serializer import TradeCreate


def create_trade(db: Session, trade: TradeCreate):
    db_trade = Trade(
        portfolio_id=trade.portfolio_id,
        asset_name=trade.asset_name,
        action=trade.action,
        price=trade.price,
        quantity=trade.quantity,
        trade_date=trade.trade_date,
    )
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade


def get_trades(db: Session):
    return db.query(Trade).all()


def get_trades_by_portfolio(db: Session, portfolio_id: int):
    return db.query(Trade).filter(Trade.portfolio_id == portfolio_id).all()


def get_trade(db: Session, trade_id: int):
    return db.query(Trade).filter(Trade.trade_id == trade_id).first()


def update_trade(db: Session, trade_id: int, trade_update: TradeCreate):
    trade = db.query(Trade).filter(Trade.trade_id == trade_id).first()
    if not trade:
        return None
    trade.asset_name = trade_update.asset_name
    trade.action = trade_update.action
    trade.price = trade_update.price
    trade.quantity = trade_update.quantity
    trade.trade_date = trade_update.trade_date
    db.commit()
    db.refresh(trade)
    return trade


def delete_trade(db: Session, trade_id: int):
    trade = db.query(Trade).filter(Trade.trade_id == trade_id).first()
    if not trade:
        return None
    db.delete(trade)
    db.commit()
    return trade
