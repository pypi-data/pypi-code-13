from . import backup
import logging
from .config import DropboxOfflineBackupConfig

def start():
    logging.getLogger('').setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    file_handler = logging.FileHandler(DropboxOfflineBackupConfig().config['DropboxBackup']['LogFile'])
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    console.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)
    logging.getLogger('').addHandler(file_handler)

    dropbox_logger = logging.getLogger("dropbox")
    dropbox_logger.setLevel(logging.WARNING)
    requests_logger = logging.getLogger("requests")
    requests_logger.setLevel(logging.WARNING)

    backup.DropboxOfflineBackup()