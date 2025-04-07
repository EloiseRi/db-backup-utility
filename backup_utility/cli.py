import argparse

from .config import set_config
from .databases.factory import DatabaseFactory
from .logger import setup_logger
from .utils import ensure_backup_dir_exists


def main():
    parser = argparse.ArgumentParser(description="DB Backup Utility")

    parser.add_argument(
        "operation", choices=["backup", "restore"], help="Operation to perform"
    )
    # TODO
    # parser.add_argument('--backup-type', required=True, choices=['full', 'incremental', 'differential'], default='full', help="Backup type specification: full, incremental, differential")

    parser.add_argument(
        "--config", type=str, required=True, help="Path to your YAML configuration file"
    )
    parser.add_argument(
        "--db-type",
        required=True,
        choices=["mysql", "postgresql", "mongodb"],
        help="Type of database to backup/restore (mysql, postgresql, mongodb)",
    )

    parser.add_argument("--cloud", type=str, help="Restore DB from a backup.")
    parser.add_argument(
        "--local-backup-dir",
        type=str,
        default="Users/eloise/backups",
        help="Restore DB from a backup.",
    )

    args = parser.parse_args()

    logger = setup_logger(__name__)
    logger.info("Starting process")

    ensure_backup_dir_exists(args.local_backup_dir)
    cfg = set_config(args.config)

    database = DatabaseFactory.database_handler(args.db_type, cfg)
    database.connect()

    try:
        if args.operation == "backup":
            database.backup("full", args.local_backup_dir)
    except Exception as e:
        logger.error(f"An error ocurred during the {args.operation} operation: {e}.")
        print(f"An error occured: {e}")

    logger.info(f"Your {args.operation} operation completed.")


if __name__ == "__main__":
    main()
