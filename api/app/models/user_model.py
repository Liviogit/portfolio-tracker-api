from sqlalchemy import Column, String
import uuid

from database import BaseSQL
from sqlalchemy.orm import relationship


class User(BaseSQL):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    # Un utilisateur peut avoir plusieurs portefeuilles
    portfolios = relationship("Portfolio", back_populates="user")
