from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from datetime import datetime
import uuid

from database import BaseSQL
from sqlalchemy.orm import relationship


class Trade(BaseSQL):
    __tablename__ = "trades"

    trade_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    portfolio_id = Column(String, ForeignKey("portfolios.portfolio_id"), nullable=False)

    asset_name = Column(String, nullable=False)
    action = Column(String, nullable=False)  # "BUY" ou "SELL"
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    trade_date = Column(DateTime, default=datetime.utcnow)

    portfolio = relationship("Portfolio", back_populates="trades")
