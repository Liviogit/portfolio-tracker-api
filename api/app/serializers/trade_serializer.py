from pydantic import BaseModel
from datetime import datetime
from typing import Optional
class TradeBase(BaseModel):
    asset_name: str
    action: str
    price: float
    quantity: int
    trade_date: datetime
    description: Optional[str] = None

class TradeCreate(BaseModel):
    portfolio_id: int
    asset_name: str
    action: str
    price: float
    quantity: int
    trade_date: Optional[datetime] = None 
    description: Optional[str] = None

class TradeRead(TradeBase):
    trade_id: int
    portfolio_id: int

    class Config:
        orm_mode = True
