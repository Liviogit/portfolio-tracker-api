from pydantic import BaseModel
from datetime import datetime

class TradeBase(BaseModel):
    asset_name: str
    action: str
    price: float
    quantity: int
    trade_date: datetime

class TradeCreate(TradeBase):
    portfolio_id: int

class TradeRead(TradeBase):
    trade_id: int
    portfolio_id: int

    class Config:
        orm_mode = True
