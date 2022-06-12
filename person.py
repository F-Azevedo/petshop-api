import datetime
import json


class Person:
    def __init__(self, person_id: int, name: str, document: int, date_of_birth: str):
        self.person_id = person_id
        self.name = name
        self.document = document
        self.date_of_birth = date_of_birth

    def toJSON(self):
        return json.dumps(self, default=lambda o: dict(year=o.year, month=o.month, day=o.day) if isinstance(o, datetime.date) else o.__dict__)

    def __str__(self):
        return f"person_id: {self.person_id}, name: {self.name}, document: {self.document}, date_of_birth: {self.date_of_birth} "


if __name__ == "__main__":
    person = Person(1, "fernando", 11111111111, "2000-01-01")
    print(person)
