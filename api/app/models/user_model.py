from sqlalchemy import Column, String,Integer
import uuid

from database import BaseSQL
from sqlalchemy.orm import relationship


class User(BaseSQL):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    # Un utilisateur peut avoir plusieurs portefeuilles
    portfolios = relationship("Portfolio", back_populates="user")
