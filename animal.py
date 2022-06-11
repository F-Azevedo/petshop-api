from enum import Enum


class Kind(Enum):
    bird = "bird"
    cat = "cat"
    dog = "dog"
    frog = "frog"
    hamster = "hamster"
    horse = "horse"
    pig = "pig"
    snake = "snake"


class Animal:
    def __init__(self, name: str, cost: float, kind: str):
        self.name = name
        self.cost = cost
        aux = kind.lower()
        for i in Kind:
            if aux == i.value:
                self.kind = aux
                print('Atribution Sucefull')
                break
        else:
            print("Atribution Failed")
            raise ValueError

    def __str__(self):
        return f"name: {self.name}, cost: {self.cost}, kind: {self.kind}"


if __name__ == '__main__':
    pet = Animal("thor", 99.99, "dog")
    print(pet)
