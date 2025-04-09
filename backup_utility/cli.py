import argparse

from .config import set_config
from .databases.factory import DatabaseFactory
from .logger import setup_logger
from .notification import send_slack_notification
from .utils import ensure_backup_dir_exists


def main():
    parser = argparse.ArgumentParser(description="DB Backup Utility")

    parser.add_argument(
        "operation", choices=["backup", "restore"], help="Operation to perform"
    )

    parser.add_argument(
        "--config", type=str, required=True, help="Path to your YAML configuration file"
    )

    parser.add_argument(
        "--local-backup-dir",
        type=str,
        default="./backups",
        help="Restore DB from a backup.",
    )

    parser.add_argument("--backup-file", help="Backup file to restore")

    args = parser.parse_args()

    logger = setup_logger(__name__)
    logger.info("Starting process")

    ensure_backup_dir_exists(args.local_backup_dir)
    cfg = set_config(args.config)

    database = DatabaseFactory.database_handler(args.db_type, cfg)

    try:
        if args.operation == "backup":
            database.backup("full", args.local_backup_dir)

            if cfg["cloud"]["enabled"]:
                if cfg["cloud"]["provider"] == "aws":
                    from .cloud.aws import upload_to_s3

                    upload_to_s3(cfg, args.local_backup_dir)
                elif cfg["cloud"]["provider"] == "azure":
                    from .cloud.azure import upload_to_azure

                    upload_to_azure(cfg, args.local_backup_dir)
                elif cfg["cloud"]["provider"] == "gcs":
                    from .cloud.gcp import upload_to_gcs

                    upload_to_gcs(cfg, args.local_backup_dir)
                else:
                    raise ValueError("Unsupported cloud provider.")
                
                if cfg['notifications']['slack']['enabled']:
                    send_slack_notification(cfg, "Backup completed successfully.")
        elif args.operation == "restore":
            database.restore(args.backup_file)
            if cfg['notifications']['slack']['enabled']:
                    send_slack_notification(cfg, "Backup completed successfully.")

    except Exception as e:
        logger.error(f"An error ocurred during the {args.operation} operation: {e}.")
        print(f"An error occured: {e}")

    logger.info(f"Your {args.operation} operation completed.")


if __name__ == "__main__":
    main()
