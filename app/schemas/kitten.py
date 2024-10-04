# -*- coding: utf-8 -*-
from typing import List
from pydantic import BaseModel, Field, PositiveInt, ConfigDict


class KittenBase(BaseModel):
    name: str = Field(min_length=1)
    age: PositiveInt
    color: str = Field(min_length=1)
    description: str = Field(min_length=1)
    breed_id: int


class KittenCreate(KittenBase):
    pass


class KittenUpdate(KittenBase):
    pass


class KittenDB(KittenBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class KittenWithBreed(BaseModel):
    breed_name: str
    kittens: List[KittenDB]
    model_config = ConfigDict(from_attributes=True)
