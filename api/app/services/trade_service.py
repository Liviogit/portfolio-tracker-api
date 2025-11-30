from sqlalchemy.orm import Session
from models.trade_model import Trade
from serializers.trade_serializer import TradeCreate
from fastapi import Depends
from database import get_db
from models.portfolio_model import Portfolio
from models.user_model import User

def create_trade(db: Session, trade: TradeCreate):
    db_trade = Trade(
        portfolio_id=trade.portfolio_id,
        asset_name=trade.asset_name.upper(),
        action=trade.action.upper(),
        price=trade.price,
        quantity=trade.quantity,
        trade_date=trade.trade_date,
    )
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade


def get_trades(
    db: Session = Depends(get_db),
    user_id: int = None
):
    # 1️⃣ Récupérer les IDs de portefeuilles de l’utilisateur connecté
    portfolio_ids = db.query(Portfolio.portfolio_id).filter(
        Portfolio.user_id == user_id
    ).all()

    # .all() renvoie une liste de tuples [(1,), (2,), ...]
    portfolio_ids = [p[0] for p in portfolio_ids]

    if not portfolio_ids:
        return []  # Aucun portefeuille → aucun trade

    # 2️⃣ Récupérer les trades liés à ces portefeuilles
    trades = db.query(Trade).filter(Trade.portfolio_id.in_(portfolio_ids)).all()
    return trades

def get_trades_by_portfolio(db: Session,user_id: int, portfolio_id: int):
    # 1️⃣ Récupérer les IDs de portefeuilles de l’utilisateur connecté
    portfolio_ids = db.query(Portfolio.portfolio_id).filter(
        Portfolio.user_id == user_id
    ).all()

    # .all() renvoie une liste de tuples [(1,), (2,), ...]
    portfolio_ids = [p[0] for p in portfolio_ids]

    if not portfolio_ids:
        return []  # Aucun portefeuille → aucun trade

    # 2️⃣ Récupérer les trades liés à ces portefeuilles
    trades = db.query(Trade).filter(Trade.portfolio_id.in_(portfolio_ids),Trade.portfolio_id == portfolio_id).all()
    return trades