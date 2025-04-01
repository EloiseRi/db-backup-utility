import logging
import psycopg2
import subprocess

from datetime import datetime
from .db_interface import IDatabase

logger = logging.getLogger(__name__)

class PostgreDatabase(IDatabase):
    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.database['host'],
                user=self.database['user'],
                password=self.database['password'],
                dbname=self.database['dbname'])

            print("Successfully connected to the database.")

        except Exception as e:
            logging.error(f"An error occured while connecting Postgresql: {e}")

    def backup(self, backup_type, backup_dir):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            output_file = f"{backup_dir}/db_backup_{timestamp}.sql"
            
            command = ["pg_dump", "-U", self.database['user'], "-F", "-c", "-b", "-v", "-f", output_file, self.database['dbname']]
            subprocess.run(command, check=True)
            logger.info(f"PostgreSQL backup of {self.database['dbname']} completed successfully, saved to {backup_dir}")
        
        except subprocess.CalledProcessError as e:
            logger.error(f"Error occured during backup of {self.database['dbname']}")
        except Exception as e:
            logger.error(f"Unexpected error during during backup process: {e}")

    def restore(self, backup_file):
        pass