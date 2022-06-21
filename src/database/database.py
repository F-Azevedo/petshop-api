import mysql.connector
from mysql.connector import Error


class Database:
    user_password = 'password'
    db_connection = ''
    db_port = 3306

    def create_server_connection(self, host_name, user_name):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                port=self.db_port,
                passwd=self.user_password
            )
            print("MySQL Database connection successfull")
        except Error as err:
            print(f"Error: {err}")
            exit(1)

        self.db_connection = connection

    def create_database(self, query):
        cursor = self.db_connection.cursor()
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
                port=self.db_port,
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
    exit(0)
