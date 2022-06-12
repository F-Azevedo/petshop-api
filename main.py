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
    query = 'SELECT * from person'
    results_query = db.read_query(query)

    result_class = []
    for i in results_query:
        result_class.append(json.loads(Person(i[0], i[1], i[2], i[3]).toJSON()))

    return {'result': result_class}


@app.get("/owners/{owner_id}", response_class=PrettyJSONResponse)
def get_one_owner(owner_id: int):
    query = 'SELECT * from person'
    results_query = db.read_query(query)
    owner = results_query[owner_id - 1]
    result = json.loads(Person(owner[0], owner[1], owner[2], owner[3]).toJSON())
    return {'result': result}