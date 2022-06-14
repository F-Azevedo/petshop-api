from pydantic import BaseModel
from typing import Union


class Person(BaseModel):
    name: str
    document: int
    dateOfBirth: str


class OptionalPerson(BaseModel):
    name: Union[str, None] = None
    document: Union[int, None] = None
    dateOfBirth: Union[str, None] = None


class Animal(BaseModel):
    name: str
    cost: float
    species: str
    owner_id: int


class OptionalAnimal(BaseModel):
    name: Union[str, None] = None
    cost: Union[float, None] = None
    species: Union[str, None] = None
    owner_id: Union[int, None] = None


class Species(BaseModel):
    name: str
