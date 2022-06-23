import re
import json
from fastapi import FastAPI, Response, status
from classes.animal import Animal
from classes.person import Person
from classes import base_model as bm
from database.database import Database
from config.json_config import PrettyJSONResponse

app = FastAPI()
db = Database()


def connect():
    db.create_db_connection("db", "root", "PETLOVE")


def validate_person(person_id, response):
    # Validating if the person exists
    query = f"""
    SELECT * FROM person WHERE person_id={person_id}
    """
    result_query = db.read_query(query)
    if not result_query:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return False, {'result': f"There is no person with id: '{person_id}'"}
    return True, {}


def validate_animal(animal_id, response):
    # Validating if the animal exists
    query = f"""
    SELECT * FROM animal WHERE animal_id={animal_id}
    """
    result_query = db.read_query(query)
    if not result_query:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return False, {'result': f"There is no pet with id: '{animal_id}'"}
    return True, {}


def validate_specie(specie, response):
    # Validating if the species exists
    query = f"""SELECT * FROM species"""
    result_query = db.read_query(query)
    available_species = []

    for i in result_query:
        available_species.append(i[0])

    if specie in available_species:
        result = f"There are no pets of this species: '{specie}'"
        valid = True
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        result = f"There is no specie with name '{specie}'"
        valid = False

    return valid, {'result': result}


def validate_date(person, response):
    # Validação para ver se a data esta em um formato válido, 1970-01-01 é uma data cursed.
    # Quando a api não recebe uma data correta no formato XXXX-XX-XX, ela a substitui por 1970-01-01.
    date_validation = re.search("\d{4}-\d{2}-\d{2}", str(person.dateOfBirth))
    if date_validation.string == '1970-01-01':
        response.status_code = status.HTTP_400_BAD_REQUEST
        return False, {'result': 'Invalid Date'}
    return True, {}


@app.get("/", response_class=PrettyJSONResponse)
def root():
    connect()
    return {"methods": "You can run the GET methods directly using the url, you can run the other methods in the 'docs' tab, or using curl directly",
            "docs": "If you want to see the documentation about the methods and the schema of the tables access 'localhost:8000/docs'.",
            "adminer": "The application is also enables adminer to access the database directly, its running in 'localhost:8080', user:root, password:password"}


# GET methods

@app.get("/owners", response_class=PrettyJSONResponse)
def get_all_owners():
    connect()

    query = 'SELECT * FROM person'
    result_query = db.read_query(query)

    if result_query:
        result = []
        for i in result_query:
            result.append(json.loads(Person(i[0], i[1], i[2], i[3]).toJSON()))
    else:
        result = "There are no owners"

    return {'result': result}


@app.get("/owners/{owner_id}", response_class=PrettyJSONResponse, status_code=200)
def get_one_owner(owner_id: int, response: Response):
    connect()

    valid, result_validation = validate_person(owner_id, response)
    if not valid:
        return result_validation

    query = f'SELECT * FROM person WHERE person_id={owner_id}'
    result_query = db.read_query(query)
    owner = result_query[0]
    result = json.loads(Person(owner[0], owner[1], owner[2], owner[3]).toJSON())
    return {'result': result}


@app.get("/owners/{owner_id}/pets", response_class=PrettyJSONResponse, status_code=200)
def get_all_pets_from_owner(owner_id: int, response: Response):
    connect()

    valid, result_validation = validate_person(owner_id, response)
    if not valid:
        return result_validation

    query = f"""
    SELECT animal.animal_id, animal.name, cost, species, person.person_id
    FROM person JOIN animal ON person.person_id=animal.owner_id
    WHERE person.person_id={owner_id}"""
    result_query = db.read_query(query)

    result = []
    for i in result_query:
        result.append(json.loads(Animal(i[0], i[1], i[2], i[3], i[4]).toJSON()))

    return {'result': result}


@app.get("/owners/{owner_id}/pets/{pet_id}", response_class=PrettyJSONResponse, status_code=200)
def get_pets_from_owner_by_pet_id(owner_id: int, pet_id: int, response: Response):
    connect()

    valid, result_validation = validate_person(owner_id, response)
    if not valid:
        return result_validation

    valid, result_validation = validate_animal(pet_id, response)
    if not valid:
        return result_validation

    query = f"""
    SELECT animal.animal_id, animal.name, cost, species, person.person_id
    FROM person JOIN animal ON person.person_id=animal.owner_id
    WHERE person.person_id={owner_id} AND animal.animal_id='{pet_id}'"""
    result_query = db.read_query(query)

    if result_query:
        result = []
        for i in result_query:
            result.append(json.loads(Animal(i[0], i[1], i[2], i[3], i[4]).toJSON()))
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        result = f"Person with id: '{owner_id}' doesn't own a pet with id: '{pet_id}'"

    return {'result': result}


@app.get("/pets", response_class=PrettyJSONResponse)
def get_all_pets():
    connect()

    query = 'SELECT * FROM animal'
    result_query = db.read_query(query)

    if result_query:
        result = []
        for i in result_query:
            result.append(json.loads(Animal(i[0], i[1], i[2], i[3], i[4]).toJSON()))
    else:
        result = "There are no pets"

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
    result_query = db.read_query(query)

    if result_query:
        result = []
        for animal, count in result_query:
            result.append({animal: count})
    else:
        result = "There are no pets"

    return {'result': result}


@app.get("/pets/{species}", response_class=PrettyJSONResponse, status_code=200)
def get_all_pets_from_specie(species: str, response: Response):
    connect()

    query = f"""SELECT * FROM animal WHERE species='{species}'"""
    result_query = db.read_query(query)

    if result_query:
        result = []
        for i in result_query:
            result.append(json.loads(Animal(i[0], i[1], i[2], i[3], i[4]).toJSON()))
        return {'result': result}
    else:
        valid, result_validation = validate_specie(species, response)
        return result_validation


@app.get("/pets/{species}/owners", response_class=PrettyJSONResponse, status_code=200)
def get_all_pet_owners_of_specie(species: str, response: Response):
    connect()

    query = f"""
    SELECT person.person_id, person.name, person.document, person.dateOfBirth, animal.animal_id, animal.name, animal.cost, animal.species, animal.owner_id
    FROM animal JOIN person ON person.person_id=animal.owner_id
    WHERE species='{species}'
    """
    result_query = db.read_query(query)

    if result_query:
        result = []
        for i in result_query:
            result.append({'owner': json.loads(Person(i[0], i[1], i[2], i[3]).toJSON()),
                           'pet': json.loads(Animal(i[4], i[5], i[6], i[7], i[8]).toJSON())})
        return {'result': result}
    else:
        valid, result_validation = validate_specie(species, response)
        return result_validation


# POST methods

@app.post("/new/person", status_code=201)
def create_person(person: bm.Person, response: Response):
    connect()

    valid, result_validation = validate_date(person, response)
    if not valid:
        return result_validation

    query = f"""
    INSERT INTO person(name, document, dateOfBirth) VALUES
    ('{person.name}', {person.document} , '{person.dateOfBirth}')
    """

    result_query = db.execute_query(query)
    if result_query == "Query successfull":
        return {'result': person}
    # Checking the error
    elif "Duplicate entry" in result_query and "for key 'person.document'" in result_query:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'result': 'Invalid Document'}


@app.post("/new/animal", status_code=201)
def create_animal(animal: bm.Animal, response: Response):
    connect()

    valid, result_validation = validate_person(animal.owner_id, response)
    if not valid:
        return result_validation

    valid, result_validation = validate_specie(animal.species, response)
    if not valid:
        return result_validation

    query = f"""
    INSERT INTO animal(name, cost, species, owner_id) VALUES
    ('{animal.name}', {animal.cost}, '{animal.species}', {animal.owner_id})
    """

    result_query = db.execute_query(query)
    if result_query == "Query successfull":
        return {'result': animal}
    # Checking the error
    elif "Duplicate entry" in result_query and "for key 'animal.UC_Animal'" in result_query:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'result': f"Person with id: '{animal.owner_id}' already has a pet of the species: '{animal.species}' with the name: '{animal.name}'"}


@app.post("/new/species", status_code=201)
def create_species(species: bm.Species, response: Response):
    connect()

    query = f"""
    INSERT INTO species VALUES
    ('{species.name}')
    """

    result_query = db.execute_query(query)
    if result_query == "Query successfull":
        return {'result': species}
    elif "Duplicate entry" in result_query and "for key 'species.PRIMARY'" in result_query:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'result': f"Specie '{species.name}' already exists"}


# DELETE methods

@app.delete("/delete/person/{person_id}", status_code=200)
def delete_person(person_id: int, response: Response):
    connect()

    valid, result_query = validate_person(person_id, response)
    if not valid:
        return result_query

    # If the user exists, proceed to delete
    query = f"""
    DELETE FROM person WHERE person_id={person_id}
    """
    db.execute_query(query)
    return {'result': f"Person with id: '{person_id}' deleted successfully"}


@app.delete("/delete/animal/{pet_id}", status_code=200)
def delete_animal(pet_id: int, response: Response):
    connect()

    valid, result_query = validate_animal(pet_id, response)
    if not valid:
        return result_query

    # If the pet exists, proceed to delete
    query = f"""
    DELETE FROM animal WHERE animal_id={pet_id}
    """
    db.execute_query(query)
    return {'result': f"Pet with id: '{pet_id}' deleted successfully"}


@app.delete("/delete/species/{name}", status_code=200)
def delete_species(name: str, response: Response):
    connect()

    valid, result_validation = validate_specie(name, response)
    if not valid:
        return result_validation

    # If the specie exists, proceed to delete
    query = f"""
    DELETE FROM species WHERE name='{name}'
    """
    db.execute_query(query)
    return {'result': f"Specie with name: '{name}' deleted successfully"}


# UPDATE methods

@app.put("/update/person/{person_id}/", status_code=200)
def update_person(person_id: int, person: bm.OptionalPerson, response: Response):
    connect()

    valid, result_validation = validate_person(person_id, response)
    if not valid:
        return result_validation

    # Verifica se não é None, pois é atributo opcional.
    if person.dateOfBirth is not None:
        valid, result_validation = validate_date(person, response)
        if not valid:
            return result_validation

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

    return {'result': f"Person with id: '{person_id}' updated successfully"}


@app.put("/update/animal/{pet_id}", status_code=200)
def update_animal(pet_id: int, animal: bm.OptionalAnimal, response: Response):
    connect()

    valid, result_validation = validate_animal(pet_id, response)
    if not valid:
        return result_validation

    if animal.owner_id:
        valid, result_validation = validate_person(animal.owner_id, response)
        if not valid:
            return result_validation

    if animal.species:
        valid, result_validation = validate_specie(animal.species, response)
        if not valid:
            return result_validation

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
