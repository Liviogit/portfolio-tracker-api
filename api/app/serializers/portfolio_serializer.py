from pydantic import BaseModel
from typing import List, Optional

class PortfolioBase(BaseModel):
    last_amount: float
    initial_amount: float
    positions: str           # Exemple : "AAPL,GOOGL,TSLA"
    positions_size: str      # Exemple : "50,30,20"

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
    positions: list[str] | None = None
    positions_size: list[int] | None = None
