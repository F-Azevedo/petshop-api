from pydantic import BaseModel


class Person(BaseModel):
    name: str
    document: int
    date_of_birth: str


class Animal(BaseModel):
    name: str
    cost: float
    species: str
    owner_id: int


class Species(BaseModel):
    name: str
