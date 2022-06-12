from animal import Animal
from database import Database
from fastapi import FastAPI
from json_config import PrettyJSONResponse
from person import Person
import json

app = FastAPI()
db = Database()
db_connection = db.create_db_connection("localhost", "root", "PETLOVE")


@app.get("/", response_class=PrettyJSONResponse)
def root():
    return {"message": "Hello World"}


@app.get("/owners", response_class=PrettyJSONResponse)
def get_all_owners():
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


@app.get("/owners/{owner_id}/pets/{animal_id}", response_class=PrettyJSONResponse)
def get_one_pets_from_owner(owner_id: int, animal_id: int):
    query = f"""
    SELECT animal.animal_id, animal.name, cost, species, person.person_id
    FROM person JOIN animal ON person.person_id=animal.owner_id
    WHERE person.person_id={owner_id} AND animal_id={animal_id}"""
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
def get_all_pets_from_specie(species: str):
    query = f"""
    SELECT person.person_id, person.name, person.document, person.dateOfBirth, animal.animal_id, animal.name, animal.cost, animal.species, animal.owner_id
    FROM animal JOIN person ON person.person_id=animal.owner_id
    WHERE species='{species}'
    """
    results_query = db.read_query(query)

    if results_query:
        result = []
        for i in results_query:
            result.append({'owner': json.loads(Person(i[0], i[1], i[2], i[3]).toJSON()), 'pet': json.loads(Animal(i[4], i[5], i[6], i[7], i[8]).toJSON())})
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
