from sqlalchemy.orm import Session
from models.portfolio_model import Portfolio
from models.user_model import User
from serializers.portfolio_serializer import PortfolioCreate, PortfolioUpdate


def create_portfolio(db: Session, portfolio: PortfolioCreate, current_user: User):
    db_portfolio = Portfolio(
        user_id=current_user.user_id,          # <-- sécurisé
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

def get_portfolios_by_user(db: Session, user_id: int, portfolio_id: int = None):
    query = db.query(Portfolio).filter(Portfolio.user_id == user_id)
    if portfolio_id is not None:
        query = query.filter(Portfolio.portfolio_id == portfolio_id)
    return query.all()

def update_portfolio(db: Session, portfolio_id: int, portfolio_update: PortfolioUpdate, user_id: int):
    portfolio= db.query(Portfolio).filter(Portfolio.user_id == user_id).filter(Portfolio.portfolio_id == portfolio_id).first()
    if not portfolio:
        return None
    portfolio.last_amount = portfolio_update.last_amount if portfolio_update.last_amount is not None else portfolio.last_amount
    portfolio.initial_amount = portfolio_update.initial_amount if portfolio_update.initial_amount is not None else portfolio.initial_amount
    portfolio.positions = portfolio_update.positions if portfolio_update.positions is not None else portfolio.positions
    portfolio.positions_size = portfolio_update.positions_size if portfolio_update.positions_size is not None else portfolio.positions_size
    db.commit()
    db.refresh(portfolio)
    return portfolio


def delete_portfolio(db: Session, portfolio_id: int, user_id: int):
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == user_id).filter(Portfolio.portfolio_id == portfolio_id).first()
    if not portfolio:
        return None
    db.delete(portfolio)
    db.commit()
    return portfolio
