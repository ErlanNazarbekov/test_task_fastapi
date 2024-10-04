from sqlalchemy import Column, String

from app.core.db import Base


class Breed(Base):
    name = Column(String, nullable=False)
