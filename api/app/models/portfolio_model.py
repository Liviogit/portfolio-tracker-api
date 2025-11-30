from sqlalchemy import Column, String, Float, ForeignKey, Integer,DateTime
from datetime import datetime
from database import BaseSQL
from sqlalchemy.orm import relationship


class Portfolio(BaseSQL):
    __tablename__ = "portfolios"

    portfolio_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)

    last_amount = Column(Float, nullable=False)
    initial_amount = Column(Float, nullable=False)
    positions = Column(String)          # ex: "AAPL,GOOGL,TSLA"
    positions_size = Column(String)     # ex: "50,30,20"
    portfolio_name = Column(String)     # ex: "Tech Stocks"
    portfolio_date = Column(DateTime, default=datetime.utcnow)    # ex: "2024-06-15 10:30:00"

    user = relationship("User", back_populates="portfolios")
    trades = relationship("Trade", back_populates="portfolio",cascade="all, delete-orphan")
