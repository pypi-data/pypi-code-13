from . import backup
import logging
from .config import DropboxOfflineBackupConfig

def start():
    logging.basicConfig(
        filename=DropboxOfflineBackupConfig().config['DropboxBackup']['LogFile'],
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    console = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)
    dropbox_logger = logging.getLogger("dropbox")
    dropbox_logger.setLevel(logging.WARNING)
    requests_logger = logging.getLogger("requests")
    requests_logger.setLevel(logging.WARNING)

    backup.DropboxOfflineBackup()