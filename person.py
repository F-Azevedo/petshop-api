from enum import Enum


class Month(Enum):
    janeiro = '1'
    fevereiro = '2'
    marco = '3'
    abril = '4'
    maio = '5'
    junho = '6'
    julho = '7'
    agosto = '8'
    setembro = '9'
    outubro = '10'
    novembro = '11'
    dezembro = '12'


class Person:
    def __init__(self, name: str, document: int, date_of_birth: str):
        self.name = name
        self.document = document

        aux = date_of_birth.split()
        print(aux)
        aux = aux[::2]
        for i in Month:
            if aux[1] == i.name:
                aux[1] = i.value
                break
        self.date_of_birth = "/".join(aux)

    def __str__(self):
        return f"name: {self.name}, document: {self.document}, date_of_birth: {self.date_of_birth}"


if __name__ == "__main__":
    person = Person("fernando", 11111111111, "01 de janeiro de 2000")
    print(person)
