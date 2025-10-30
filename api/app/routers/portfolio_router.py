from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from services.portfolio_service import (
    create_portfolio, get_portfolios, get_portfolio, update_portfolio, delete_portfolio, get_portfolios_by_user
)
from serializers.portfolio_serializer import PortfolioCreate, PortfolioRead

portfolio_router = APIRouter(prefix="/portfolios", tags=["portfolios"])


@portfolio_router.post("/", response_model=PortfolioRead)
def create_portfolio_endpoint(portfolio: PortfolioCreate, db: Session = Depends(get_db)):
    return create_portfolio(db, portfolio)


@portfolio_router.get("/", response_model=list[PortfolioRead])
def read_portfolios(db: Session = Depends(get_db)):
    return get_portfolios(db)


@portfolio_router.get("/user/{user_id}", response_model=list[PortfolioRead])
def read_portfolios_by_user(user_id: int, db: Session = Depends(get_db)):
    return get_portfolios_by_user(db, user_id)


@portfolio_router.get("/{portfolio_id}", response_model=PortfolioRead)
def read_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    portfolio = get_portfolio(db, portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio


@portfolio_router.put("/{portfolio_id}", response_model=PortfolioRead)
def update_portfolio_endpoint(portfolio_id: int, portfolio_update: PortfolioCreate, db: Session = Depends(get_db)):
    portfolio = update_portfolio(db, portfolio_id, portfolio_update)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio


@portfolio_router.delete("/{portfolio_id}", response_model=PortfolioRead)
def delete_portfolio_endpoint(portfolio_id: int, db: Session = Depends(get_db)):
    portfolio = delete_portfolio(db, portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio
