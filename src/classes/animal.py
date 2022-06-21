import json


class Animal:
    def __init__(self, animal_id: int, name: str, cost: float, species: str, owner_id: int):
        self.animal_id = animal_id
        self.name = name
        self.cost = cost
        self.species = species
        self.owner_id = owner_id

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __str__(self):
        return f"name: {self.name}, cost: {self.cost}, species: {self.species}, owner: {self.owner_id}"


if __name__ == '__main__':
    pet = Animal(1, "thor", 99.99, "dog", 1)
    print(pet)
