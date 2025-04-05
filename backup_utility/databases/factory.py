from .mongodb import MongoDatabase
from .mysql import MySQLDatabase
from .postgresql import PostgreDatabase


class DatabaseFactory:
    def database_handler(db_type, config):
        db_types = {
            "postgresql": PostgreDatabase,
            "mysql": MySQLDatabase,
            "mongodb": MongoDatabase,
        }
        if db_type not in db_types:
            raise ValueError(f"Unsupported database type: {db_type}")
        return db_types[db_type](config)
