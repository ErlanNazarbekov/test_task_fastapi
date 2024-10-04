from pydantic import BaseModel, Field, ConfigDict


class BreedBase(BaseModel):
    name: str = Field(min_length=1)


class BreedCreate(BreedBase):
    pass


class BreedDB(BreedBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
