import logging
import os

logger = logging.getLogger(__name__)


def ensure_backup_dir_exists(backupdir):
    if not os.path.exists(backupdir):
        try:
            os.makedirs(backupdir)
            logger.info((f"Backup directory '{backupdir}' was created."))
        except Exception as e:
            logger.error(f"Failed to create backup directory '{backupdir}': {e}")
            raise
    else:
        logger.info(f"Backup directory '{backupdir}' already exists.")
