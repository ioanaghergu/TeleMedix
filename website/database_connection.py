import pyodbc

class DatabaseConnection:
    _instance = None

    def __new__(cls, server, database, username, password, driver="{ODBC Driver 18 for SQL Server}"):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = None
            cls._instance.connection_string = (
                f"DRIVER={driver};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"UID={username};"
                f"PWD={password}"
            )
        return cls._instance

    def get_connection(self):
        if self.connection is None:
            try:
                self.connection = pyodbc.connect(self.connection_string)
                print("Database connection established")
            except Exception as e:
                print("Database connection failed:", e)
                self.connection = None
        return self.connection
