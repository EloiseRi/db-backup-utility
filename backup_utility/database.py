import logging
import mysql.connector
import subprocess

from mysql.connector import Error
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class DatabaseFactory:
    def database_handler(db_type, config):
        db_types = {
            "postgresql": Postgres,
            "mysql": MySQL,
            "mongodb": MongoDB,
        }
        if db_type not in db_types:
            raise ValueError(f"Unsupported database type: {db_type}")
        return db_types[db_type](config)

class Database(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def backup(self, backup_type, output_path):
        pass

    @abstractmethod
    def restore(self, backup_file):
        pass

class Postgres(Database):
    def connect(self):
        print(f"Connection to PostgreSQL at {self.config['database']['host']}...")

    def backup(self, backup_type, output_path):
        pass

    def restore(self, backup_file):
        pass

class MySQL(Database):
    def connect(self):
        try:
            print(f"Connection to MySQL at {self.config['database']['host']}...")
            conn = mysql.connector.connect(
                host=self.config['database']['host'],
                port=self.config['database']['port'],
                user=self.config['database']['user'],
                password=self.config['database']['password'],
                database=self.config['database']['dbname']
            )

            if conn.is_connected():
                logger.info(f"Successfully connected to the database.")
                return conn
        except Error as e:
            logger.error(f"Error: {e}")

    def backup(self, backup_type, output_path):
        try:
            command = ["mysqldump", "-u", self.config['database']['user'], f"-p{self.config['database']['password']}", self.config['database']['dbname'], f"> {output_path}"]
            subprocess.run(command, check=True)

            logger.info(f"MySQL backup of {self.config['database']['dbname']} completed successfully, saved to {output_path}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error occured during backup of {self.config['database']['dbname']}")
        except Exception as e:
            logger.error(f"Unexpected error during during backup process: {e}")

    def restore(self, backup_file):
        pass

class MongoDB(Database):
    def connect(self):
        print(f"Connection to MongoDB at {self.config['database']['host']}...")

    def backup(self, backup_type, output_path):
        pass

    def restore(self, backup_file):
        pass