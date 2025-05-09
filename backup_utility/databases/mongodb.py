import gzip
import os
import subprocess
import pymongo

from datetime import datetime
from .db_interface import IDatabase
from ..logger import setup_logger

logger = setup_logger(__name__)

class MongoDatabase(IDatabase):
    def connect(self):
        try:
            print(f"Connection to MongoDB at {self.database['host']}...")
            conn = pymongo.MongoClient(
                f"mongodb://{self.database['host']}:{self.database['port']}/"
            )

            conn.admin.command("ping")
            logger.info(f"Successfully connected to the database.")
            self.conn = conn

        except Exception as e:
            logger.error(f"An error occured: {e}")

    def backup(self, backup_type, backup_dir):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            output_file = f"{backup_dir}/db_backup_{timestamp}.sql"
            command = [
                "mongodump",
                "--host",
                self.database["host"],
                "--port",
                str(self.database["port"]),
                "--username",
                self.database["user"],
                "--password",
                self.database["password"],
                "--authenticationDatabase",
                "admin",
                "--db",
                self.database["dbname"],
                "--out",
                output_file,
            ]
            
            if self.config['backup'].get('compress', False):
                    self._compress_backup(output_file)

            subprocess.run(command, check=True)
            logger.info(
                f"MongoDB backup of {self.database['dbname']} completed successfully, saved to {backup_dir}"
            )


        except subprocess.CalledProcessError as e:
            logger.error(f"Error occured during backup of {self.database['dbname']}")
        except Exception as e:
            logger.error(f"Unexpected error during during backup process: {e}")

    def _compress_backup(self, output_file):
        try:
            with open(output_file, "rb") as f_in:
                compressed_file = f"{output_file}.gz"
                with gzip.open(compressed_file, "wb") as f_out:
                    f_out.writelines(f_in)

            os.remove(output_file)
            logger.info(f"Backup file compressed successfully: {compressed_file}")
        except Exception as e:
            logger.error(f"Error occurred during compression of {output_file}: {e}")

    def restore(self, backup_file):
        try:
            command = [
                "mongorestore",
                "--host",
                self.database["host"],
                "--port",
                str(self.database["port"]),
                "--username",
                self.database["username"],
                "--password",
                self.database["password"],
                "--authenticationDatabase",
                "admin",
                "--dbname",
                self.database["dbname"],
                backup_file,
            ]

            subprocess.run(command, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error occured during backup of {self.database['dbname']}")
        except Exception as e:
            logger.error(f"Unexpected error during during backup process: {e}")
