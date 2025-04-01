import logging
import subprocess
import pymongo

from datetime import datetime
from .db_interface import IDatabase

logger = logging.getLogger(__name__)

class MongoDatabase(IDatabase):
    def connect(self):
        try:
            print(f"Connection to MongoDB at {self.database['host']}...")
            conn = pymongo.MongoClient(f"mongodb://{self.database['host']}:{self.database['port']}/")

            conn.admin.command('ping')
            logger.info(f"Successfully connected to the database.")
            self.conn = conn

        except Exception as e:
            logger.error(f"An error occured: {e}")
         
    def backup(self, backup_type, backup_dir):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            output_file = f"{backup_dir}/db_backup_{timestamp}.sql"
            command = ["mongodump", "--db", self.database['dbname'], "--out", output_file]

            subprocess.run(command, check=True)
            logger.info(f"MongoDB backup of {self.database['dbname']} completed successfully, saved to {backup_dir}")
        
        except subprocess.CalledProcessError as e:
            logger.error(f"Error occured during backup of {self.database['dbname']}")
        except Exception as e:
            logger.error(f"Unexpected error during during backup process: {e}")            

    def restore(self, backup_file):
        pass