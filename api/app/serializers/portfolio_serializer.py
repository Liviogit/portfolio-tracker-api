from pydantic import BaseModel
from typing import List, Optional
import datetime
class PortfolioBase(BaseModel):
    portfolio_id: Optional[int] = None
    last_amount: float
    initial_amount: float
    positions: str           # Exemple : "AAPL,GOOGL,TSLA"
    positions_size: str      # Exemple : "50,30,20"
    portfolio_name: str
    portfolio_date: Optional[datetime.datetime] = None
    cash_balance: float
class PortfolioCreate(PortfolioBase):
    pass

class PortfolioRead(PortfolioBase):
    portfolio_id: int
    user_id: int

    class Config:
        orm_mode = True

class PortfolioUpdate(BaseModel):
    last_amount: float | None = None
    initial_amount: float | None = None
    positions: str | None = None
    positions_size: str | None = None
    portfolio_name: str | None = None
    cash_balance: float | None = None
