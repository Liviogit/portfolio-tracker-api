from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.user_model import User
from services.auth_service import get_current_user
from database import get_db
from services.portfolio_service import (
    create_portfolio, get_portfolios_by_user, update_portfolio, delete_portfolio
)
from serializers.portfolio_serializer import PortfolioCreate, PortfolioRead

portfolio_router = APIRouter(prefix="/portfolios", tags=["portfolios"])


@portfolio_router.post("/", response_model=PortfolioRead)
def create_portfolio_endpoint(
    portfolio: PortfolioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # récupère l'utilisateur connecté
):
    return create_portfolio(db, portfolio, current_user)

@portfolio_router.get("/", response_model=list[PortfolioRead])
def get_my_portfolios(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retourne uniquement les portefeuilles de l'utilisateur connecté.
    """
    return get_portfolios_by_user(db, current_user.user_id)

@portfolio_router.get("/{portfolio_id}", response_model=list[PortfolioRead])
def get_my_portfolios_id(portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    
):
    """
    Retourne uniquement les portefeuilles de l'utilisateur connecté.
    """
    return get_portfolios_by_user(db, current_user.user_id, portfolio_id=portfolio_id)

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
