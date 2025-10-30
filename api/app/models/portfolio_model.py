from sqlalchemy import Column, String, Float, ForeignKey
import uuid

from database import BaseSQL
from sqlalchemy.orm import relationship


class Portfolio(BaseSQL):
    __tablename__ = "portfolios"

    portfolio_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)

    last_amount = Column(Float, nullable=False)
    initial_amount = Column(Float, nullable=False)
    positions = Column(String)          # ex: "AAPL,GOOGL,TSLA"
    positions_size = Column(String)     # ex: "50,30,20"

    user = relationship("User", back_populates="portfolios")
    trades = relationship("Trade", back_populates="portfolio")
