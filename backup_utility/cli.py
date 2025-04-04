import argparse
import logging
import os

<<<<<<< HEAD:backup_utility/cli.py
from .databases.factory import DatabaseFactory
from .config import set_config
from .utils import ensure_backup_dir_exists
=======
from database import DatabaseFactory, MySQL
from config import set_config
from utils import ensure_backup_dir_exists
>>>>>>> origin/dev:backup-utility/cli.py

def setup_logger(log_file):

    logging.basicConfig(
        level=logging.INFO, # INFO type and above will be displayed in the console
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    file_handler = logging.FileHandler(log_file, mode="a")
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    logging.info(f"Logger initialized. Log file : {log_file}")

def main():
    parser = argparse.ArgumentParser(description="DB Backup Utility")

    parser.add_argument('operation', choices=['backup', 'restore'], help="Operation to perform")
    # TODO
    # parser.add_argument('--backup-type', required=True, choices=['full', 'incremental', 'differential'], default='full', help="Backup type specification: full, incremental, differential")

    parser.add_argument('--config', type=str, required=True, help="Path to your YAML configuration file")
    parser.add_argument('--db-type', required=True, choices=['mysql', 'postgresql', 'mongodb'], help="Type of database to backup/restore (mysql, postgresql, mongodb)")
    
    parser.add_argument('--cloud', type=str, help="Restore DB from a backup.")
    parser.add_argument('--local-backup-dir', type=str, default='/backups', help="Restore DB from a backup.")

    parser.add_argument('--log-file', help="Path to the log file", default="db-backup.log")

    args = parser.parse_args()

    setup_logger(args.log_file)
    logger = logging.getLogger(__name__)

    ensure_backup_dir_exists(args.local_backup_dir)
    cfg = set_config(args.config)

    database = DatabaseFactory.database_handler(args.db_type, cfg)
    database.connect()

    try:
        if args.operation == 'backup':
            database.backup("full", args.local_backup_dir)
    except Exception as e:
        logging.error(f"An error ocurred during the {args.operation} operation: {e}.")
        print(f"An error occured: {e}")

    logging.info(f"Your {args.operation} operation completed.")
if __name__ == "__main__":
    main()