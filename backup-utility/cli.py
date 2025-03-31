import argparse
import logging
import os

from utils import ensure_backup_dir_exists

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

    parser.add_argument('--config', type=str, required=True, help="Path to your YAML configuration file")
    parser.add_argument('--db-type', required=True, choices=['mysql', 'postgresql', 'mongodb'], help="Type of database to backup/restore (mysql, postgresql, mongodb)")
    
    parser.add_argument('--cloud', type=str, help="Restore DB from a backup.")
    parser.add_argument('--local-backup-dir', type=str, default='/backups', help="Restore DB from a backup.")
    parser.add_argument('--dry-run', action='store_true', help="Test the backup/restore without making changes")

    parser.add_argument('--log-file', help="Path to the log file", default="db-backup.log")

    args = parser.parse_args()

    setup_logger(args.log_file)
    ensure_backup_dir_exists(args.local_backup_dir)
    