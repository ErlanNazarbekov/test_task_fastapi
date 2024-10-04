from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base


class Kitten(Base):
    name = Column(String, unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    color = Column(String, nullable=False)
    description = Column(Text, nullable=False)

    breed_id = Column(Integer, ForeignKey('breed.id'))
    breed = relationship('Breed')
