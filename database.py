import mysql.connector
from mysql.connector import Error


class Database:
    user_password = '123'
    db_connection = ''

    def create_server_connection(self, host_name, user_name):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=self.user_password
            )
            print("MySQL Database connection successfull")
        except Error as err:
            print(f"Error: {err}")

        return connection

    def create_database(self, connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            print("Database created successfully")
        except Error as err:
            print(f"Error: {err}")

    def create_db_connection(self, host_name, user_name, db_name):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=self.user_password,
                database=db_name
            )
            print("MySQL Database connection successfull")
        except Error as err:
            print(f"Error: {err}")

        self.db_connection = connection

    def execute_query(self, query):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute(query)
            self.db_connection.commit()
            return "Query successfull"
        except Error as err:
            return f"Error: {err}"

    def read_query(self, query):
        cursor = self.db_connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as err:
            print(f"Error: '{err}'")


if __name__ == "__main__":
    db = Database()
    db_connection = db.create_server_connection("localhost", "root")

    # Criando base de dados
    create_db_query = """
    DROP DATABASE IF EXISTS PETLOVE;
    CREATE DATABASE PETLOVE;
    """
    db.create_database(db_connection, create_db_query)

    # Conectando a base de dados
    db.create_db_connection("localhost", "root", "PETLOVE")

    # Criando as tabelas
    create_person_table = """
    CREATE TABLE person(
    person_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    document INT NOT NULL UNIQUE,
    dateOfBirth DATE,
    PRIMARY KEY (person_id)
    );
    """
    create_animal_table = """
    CREATE TABLE animal(
    animal_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    cost FLOAT NOT NULL,
    species VARCHAR(50) NOT NULL,
    owner_id INT NOT NULL,
    PRIMARY KEY (animal_id),
    CONSTRAINT UC_Animal UNIQUE (name, species, owner_id)
    );
    """

    create_species_table = """
    CREATE TABLE species(
    name VARCHAR(50) NOT NULL,
    PRIMARY KEY (name)
    );
    """

    if db.execute_query(create_person_table) != "Query successfull":
        print("Erro in create_person_table")
        exit()
    elif db.execute_query(create_species_table) != "Query successfull":
        print("Erro in create_species_table")
        exit()
    elif db.execute_query(create_animal_table) != "Query successfull":
        print(db.execute_query(create_animal_table))
        print("Erro in create_animal_table")
        exit()

    print("Table creation successfull!")

    # Definindo as chaves extrangeiras

    alter_animal = """
    ALTER TABLE animal
    ADD FOREIGN KEY(owner_id)
    REFERENCES person(person_id)
    ON DELETE CASCADE
    """

    if db.execute_query(alter_animal) != "Query successfull":
        print("Erro adding OWNER_ID foreing key in animal table")
        exit()

    alter_animal = """
    ALTER TABLE animal
    ADD FOREIGN KEY(species)
    REFERENCES species(name)
    ON DELETE CASCADE
    """

    if db.execute_query(alter_animal) != "Query successfull":
        print("Erro adding SPECIES foreing key in animal table")
        exit()

    print("Foreign Keys creation successfull")

    # Populando base de dados

    populate_person = """
    INSERT INTO person(name, document, dateOfBirth) VALUES
    ('Fernando Azevedo', 1, '2000-01-01'),
    ('Danilo Erler', 2, '2001-03-03'),
    ('Phineas Flynn Fletcher', 3, '1990-07-19');
    """

    populate_species = """
    INSERT INTO species VALUES
    ('beaver'),
    ('cat'),
    ('cow'),
    ('dog'),
    ('fish'),
    ('frog'),
    ('hamster'),
    ('horse'),
    ('iguana'),
    ('llama'),
    ('parrot'),
    ('pig'),
    ('platypus'),
    ('snake');
    """

    populate_animal = """
    INSERT INTO animal(name, cost, species, owner_id) VALUES
    ('Perry', 199.99, 'platypus', 3),
    ('Kate', 299.99, 'dog', 1),
    ('Link', 0.99, 'fish', 2),
    ('Willow', 399.99, 'iguana', 3),
    ('Dolina', 199.99, 'horse', 1),
    ('Bezie', 199.99, 'cow', 2),
    ('Urbi', 199.99, 'platypus', 3),
    ('Ladylou', 199.99, 'snake', 1);
    """

    if db.execute_query(populate_person) != "Query successfull":
        print("Erro in populate_person")
        exit()
    elif db.execute_query(populate_species) != "Query successfull":
        print("Erro in populate_species")
        exit()
    elif db.execute_query(populate_animal) != "Query successfull":
        print("Erro in populate_animal")
        exit()

    print("Populating database successfull")
