import gzip
import os
import psycopg2
import subprocess

from datetime import datetime
from ..logger import setup_logger
from .db_interface import IDatabase

logger = setup_logger(__name__)


class PostgreDatabase(IDatabase):
    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.database["host"],
                user=self.database["user"],
                password=self.database["password"],
                dbname=self.database["dbname"],
            )

            print("Successfully connected to the database.")

        except Exception as e:
            logger.error(f"An error occured while connecting Postgresql: {e}")

    def backup(self, backup_type, backup_dir):
        try:
            env = os.environ.copy()
            env["PGPASSWORD"] = self.database["password"]

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            output_file = f"{backup_dir}/db_backup_{timestamp}.dump"

            command = [
                "pg_dump",
                "-h",
                self.database["host"],
                "-p",
                "5432",
                "-U",
                self.database["user"],
                "-F",
                "c",
                "-b",
                "-v",
                "-f",
                output_file,
                self.database["dbname"],
            ]

            subprocess.run(command, env=env, check=True)

            if self.config['backup'].get('compress', False):
                    self._compress_backup(output_file)

            logger.info(
                f"PostgreSQL backup of {self.database['dbname']} completed successfully, saved to {backup_dir}"
            )

        except subprocess.CalledProcessError as e:
            logger.error(f"Error occured during backup of {self.database['dbname']}")
        except Exception as e:
            logger.error(f"Unexpected error during backup process: {e}")

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
            env = os.environ.copy()
            env["PGPASSWORD"] = self.database["password"]

            command = [
                "pg_restore",
                "--host",
                self.database["host"],
                "--port",
                str(self.database["port"]),
                "--username",
                self.database["username"],
                "--password",
                self.database["password"],
                "--dbname",
                self.database["dbname"],
                backup_file,
            ]

            subprocess.run(command, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error occured during restore of {self.database['dbname']}")
        except Exception as e:
            logger.error(f"Unexpected error during restore process: {e}")
