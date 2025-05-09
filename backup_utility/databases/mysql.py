import gzip
import os
import mysql.connector
import subprocess

from datetime import datetime
from .db_interface import IDatabase
from ..logger import setup_logger
from mysql.connector import Error

logger = setup_logger(__name__)

class MySQLDatabase(IDatabase):
    def connect(self):
        try:
            print(f"Connection to MySQL at {self.database['host']}...")
            conn = mysql.connector.connect(
                host=self.database["host"],
                port=self.database["port"],
                user=self.database["user"],
                password=self.database["password"],
                database=self.database["dbname"],
            )

            if conn.is_connected():
                logger.info("Successfully connected to the database.")
                self.conn = conn
        except Error as e:
            logger.error(f"An error occured: {e}")

    def backup(self, backup_type, backup_dir):
        try:
            if backup_type == "full":
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                output_file = f"{backup_dir}/db_backup_{timestamp}.sql"
                command = [
                    "mysqldump",
                    "-h",
                    self.database["host"],
                    "-u",
                    self.database["user"],
                    f"-p{self.database['password']}",
                    self.database["dbname"],
                ]  # Need to add --protocol=tcp if using docker-compose dev_env

                with open(output_file, "w") as file:
                    subprocess.run(command, stdout=file, check=True)

                if self.config['backup'].get('compress', False):
                    self._compress_backup(output_file)

            elif backup_type == "incremental":
                # TODO
                pass

            elif backup_type == "differential":
                # TODO
                pass

            logger.info(
                f"MySQL backup of {self.database['dbname']} completed successfully, saved to {backup_dir}"
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
            with open(backup_file) as file:
                command = [
                    "mysql",
                    "-h",
                    self.database["host"],
                    "-u",
                    self.database["user"],
                    "-p" + self.database["password"],
                    self.database["dbname"],
                ]
                subprocess.run(command, stdin=file, check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"MySQL restore failed: {e}")
            raise RuntimeError(f"MySQL restore failed: {e}") from e
        except FileNotFoundError:
            logger.error(f"Dump file not found: {backup_file}")
        except Exception as e:
            logger.error(f"Unexpected error during during backup process: {e}")
            raise
