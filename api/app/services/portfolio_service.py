from sqlalchemy.orm import Session
from models.portfolio_model import Portfolio
from serializers.portfolio_serializer import PortfolioCreate


def create_portfolio(db: Session, portfolio: PortfolioCreate):
    db_portfolio = Portfolio(
        user_id=portfolio.user_id,
        last_amount=portfolio.last_amount,
        initial_amount=portfolio.initial_amount,
        positions=portfolio.positions,
        positions_size=portfolio.positions_size,
    )
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio

def get_portfolios_by_user(db: Session, user_id: int):
    return db.query(Portfolio).filter(Portfolio.user_id == user_id).all()

def update_portfolio(db: Session, portfolio_id: int, portfolio_update: PortfolioCreate):
    portfolio = db.query(Portfolio).filter(Portfolio.portfolio_id == portfolio_id).first()
    if not portfolio:
        return None
    portfolio.last_amount = portfolio_update.last_amount
    portfolio.initial_amount = portfolio_update.initial_amount
    portfolio.positions = portfolio_update.positions
    portfolio.positions_size = portfolio_update.positions_size
    db.commit()
    db.refresh(portfolio)
    return portfolio


def delete_portfolio(db: Session, portfolio_id: int):
    portfolio = db.query(Portfolio).filter(Portfolio.portfolio_id == portfolio_id).first()
    if not portfolio:
        return None
    db.delete(portfolio)
    db.commit()
    return portfolio
