import re
import json
from fastapi import FastAPI
from classes.animal import Animal
from classes.person import Person
from classes import base_model as bm
from database.database import Database
from config.json_config import PrettyJSONResponse

app = FastAPI()
db = Database()


def connect():
    db.create_db_connection("db", "root", "PETLOVE")


@app.get("/", response_class=PrettyJSONResponse)
def root():
    connect()
    return {"message": "Hello World"}


# GET methods

@app.get("/owners", response_class=PrettyJSONResponse)
def get_all_owners():
    connect()
    query = 'SELECT * FROM person'
    results_query = db.read_query(query)

    if results_query:
        result = []
        for i in results_query:
            result.append(json.loads(Person(i[0], i[1], i[2], i[3]).toJSON()))
    else:
        result = "There are no owners."

    return {'result': result}


@app.get("/owners/{owner_id}", response_class=PrettyJSONResponse)
def get_one_owner(owner_id: int):
    connect()
    query = f'SELECT * FROM person WHERE person_id={owner_id}'
    result_query = db.read_query(query)
    if result_query:
        owner = result_query[0]
        result = json.loads(Person(owner[0], owner[1], owner[2], owner[3]).toJSON())
    else:
        result = "There is no such owner."
    return {'result': result}


@app.get("/owners/{owner_id}/pets", response_class=PrettyJSONResponse)
def get_all_pets_from_owner(owner_id: int):
    connect()
    query = f"""
    SELECT animal.animal_id, animal.name, cost, species, person.person_id
    FROM person JOIN animal ON person.person_id=animal.owner_id
    WHERE person.person_id={owner_id}"""
    results_query = db.read_query(query)

    if results_query:
        result = []
        for i in results_query:
            result.append(json.loads(Animal(i[0], i[1], i[2], i[3], i[4]).toJSON()))
    else:
        result = "There is no such owner."

    return {'result': result}


@app.get("/owners/{owner_id}/pets/{pet_id}", response_class=PrettyJSONResponse)
def get_pets_from_owner_by_pet_id(owner_id: int, pet_id: int):
    connect()
    query = f"""
    SELECT animal.animal_id, animal.name, cost, species, person.person_id
    FROM person JOIN animal ON person.person_id=animal.owner_id
    WHERE person.person_id={owner_id} AND animal.animal_id='{pet_id}'"""
    results_query = db.read_query(query)

    if results_query:
        result = []
        for i in results_query:
            result.append(json.loads(Animal(i[0], i[1], i[2], i[3], i[4]).toJSON()))
    else:
        result = "There is no such pet."

    return {'result': result}


@app.get("/pets", response_class=PrettyJSONResponse)
def get_all_pets():
    connect()
    query = 'SELECT * FROM animal'
    results_query = db.read_query(query)

    if results_query:
        result = []
        for i in results_query:
            result.append(json.loads(Animal(i[0], i[1], i[2], i[3], i[4]).toJSON()))
    else:
        result = "There are no pets."

    return {'result': result}


@app.get("/pets/count", response_class=PrettyJSONResponse)
def get_count_pets_by_species():
    connect()
    query = """
    SELECT species.name, count(animal.species)
    FROM species LEFT JOIN animal ON species.name=animal.species
    GROUP BY species.name
    ORDER BY count(animal.species) DESC, species.name
    """
    results_query = db.read_query(query)

    if results_query:
        result = []
        for animal, count in results_query:
            result.append({animal: count})
    else:
        result = "There are no pets."

    return {'result': result}


@app.get("/pets/{species}", response_class=PrettyJSONResponse)
def get_all_pets_from_specie(species: str):
    connect()
    query = f"""SELECT * FROM animal WHERE species='{species}'"""
    results_query = db.read_query(query)

    if results_query:
        result = []
        for i in results_query:
            result.append(json.loads(Animal(i[0], i[1], i[2], i[3], i[4]).toJSON()))
    else:
        query = f"""SELECT * FROM species"""
        results_query = db.read_query(query)
        available_species = []

        for i in results_query:
            available_species.append(i[0])

        if species in available_species:
            result = f"There are no pets of this species: ({species})"
        else:
            result = f"({species}) is not in the species list."

    return {'result': result}


@app.get("/pets/{species}/owners", response_class=PrettyJSONResponse)
def get_all_pet_owners_of_specie(species: str):
    connect()
    query = f"""
    SELECT person.person_id, person.name, person.document, person.dateOfBirth, animal.animal_id, animal.name, animal.cost, animal.species, animal.owner_id
    FROM animal JOIN person ON person.person_id=animal.owner_id
    WHERE species='{species}'
    """
    results_query = db.read_query(query)

    if results_query:
        result = []
        for i in results_query:
            result.append({'owner': json.loads(Person(i[0], i[1], i[2], i[3]).toJSON()),
                           'pet': json.loads(Animal(i[4], i[5], i[6], i[7], i[8]).toJSON())})
    else:
        query = f"""SELECT * FROM species"""
        results_query = db.read_query(query)
        available_species = []

        for i in results_query:
            available_species.append(i[0])

        if species in available_species:
            result = f"There are no pets of this species: ({species})"
        else:
            result = f"({species}) is not in the species list."

    return {'result': result}


# POST methods

@app.post("/new/person")
def create_person(person: bm.Person):
    connect()
    # Validação para ver se a data esta em um formato válido, 1970-01-01 é uma data cursed.
    # Quando a api não recebe uma data correta no formato XXXX-XX-XX, ela a substitui por 1970-01-01.
    date_validation = re.search("\d{4}-\d{2}-\d{2}", str(person.dateOfBirth))
    if date_validation.string == '1970-01-01':
        return {'result': 'Invalid Date'}

    query = f"""
    INSERT INTO person(name, document, dateOfBirth) VALUES
    ('{person.name}', {person.document} , '{person.dateOfBirth}')
    """

    result_query = db.execute_query(query)
    if result_query == "Query successfull":
        return {'result': person}

    return {'result': result_query}


@app.post("/new/animal")
def create_animal(animal: bm.Animal):
    connect()
    query = f"""
    INSERT INTO animal(name, cost, species, owner_id) VALUES
    ('{animal.name}', {animal.cost}, '{animal.species}', {animal.owner_id})
    """

    result_query = db.execute_query(query)
    if result_query == "Query successfull":
        return {'result': animal}

    return {'result': result_query}


@app.post("/new/species")
def create_species(species: bm.Species):
    connect()
    query = f"""
    INSERT INTO species VALUES
    ('{species.name}')
    """

    result_query = db.execute_query(query)
    if result_query == "Query successfull":
        return {'result': species}

    return {'result': result_query}


# DELETE methods

@app.delete("/delete/person/{person_id}")
def delete_person(person_id: int):
    connect()
    query = f"""
    DELETE
    FROM person
    WHERE person_id={person_id}
    """

    result_query = db.execute_query(query)

    return {'result': result_query}


@app.delete("/delete/animal/{pet_id}")
def delete_animal(pet_id: int):
    connect()
    query = f"""
    DELETE
    FROM animal
    WHERE animal_id={pet_id}
    """

    result_query = db.execute_query(query)

    return {'result': result_query}


@app.delete("/delete/species/{name}")
def delete_species(name: str):
    connect()
    query = f"""
    DELETE
    FROM species
    WHERE name='{name}'
    """

    result_query = db.execute_query(query)

    return {'result': result_query}


# UPDATE methods

@app.put("/update/person/{person_id}/")
def update_person(person_id: int, person: bm.OptionalPerson):
    connect()
    # Validação para ver se a data esta em um formato válido, 1970-01-01 é uma data cursed.
    # Quando a api não recebe uma data correta no formato XXXX-XX-XX, ela a substitui por 1970-01-01.
    # Verifica se não é None, pois é atributo opcional.
    if person.dateOfBirth is not None:
        date_validation = re.search("\d{4}-\d{2}-\d{2}", str(person.dateOfBirth))
        if date_validation.string == '1970-01-01':
            return {'result': 'Invalid Date'}

    var = "SET"
    for key, value in person:
        if value:
            if var == 'SET':
                var += f' {key} = "{value}"'
            else:
                var += f', {key} = "{value}"'

    query = f"""
    UPDATE person
    {var}
    WHERE person_id={person_id}
    """

    result_query = db.execute_query(query)

    return {'result': result_query}


@app.put("/update/animal/{pet_id}")
def update_animal(pet_id: int, animal: bm.OptionalAnimal):
    connect()
    var = "SET"
    for key, value in animal:
        if value:
            if var == 'SET':
                var += f' {key} = "{value}"'
            else:
                var += f', {key} = "{value}"'

    query = f"""
    UPDATE animal
    {var}
    WHERE animal_id={pet_id}
    """

    result_query = db.execute_query(query)

    return {'result': result_query}
