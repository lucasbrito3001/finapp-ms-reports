import psycopg2


class DatabaseCursor:
    def __init__(self, cursor):
        self.cursor = cursor

    def run_dml_query(self, query, values):
        print(f"[DatabaseConnection] Running DML query: {query}")
        self.cursor.execute(query, values)
        
        self.cursor.commit()
        return

    def run_dql_query(self, query, values):
        print(f"[DatabaseConnection] Running DQL query: {query}")
        self.cursor.execute(query, values)
        
        result = self.cursor.fetchall()
        
        return result


class DatabaseConnection:
    def __init__(self, connection) -> None:
        self.connection = connection

    def create_cursor(self):
        print("[DatabaseConnection] Creating cursor to run queries")
        cursor = self.connection.cursor()
        return DatabaseCursor(cursor)


class DatabaseConnector:
    connection = DatabaseConnection

    def connect(self, connection_string: str):
        print("[DatabaseConnection] Connecting to database")
        self.connection = psycopg2.connect(connection_string)
        return DatabaseConnection(self.connection)

    def disconnect(self):
        self.connection.close()
