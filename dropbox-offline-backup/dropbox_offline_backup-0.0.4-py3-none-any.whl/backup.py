import concurrent.futures
import datetime
import logging
import os
import pathlib
import pickle
import dropbox

from .config import DropboxOfflineBackupConfig


class DropboxOfflineBackup:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.config = DropboxOfflineBackupConfig().config
        self.dbx = dropbox.Dropbox(self.config['DropboxBackup']['AccessToken'])
        self.destination_folder = os.path.join(self.config['DropboxBackup']['BackupDestinationPath'],
                                               datetime.datetime.now().strftime("%Y.%m.%d.%H.%M.%S"))
        self.threads = self.config['DropboxBackup']['ConcurrentThreads']
        self.reuse_entries = False

        if not os.path.exists(self.destination_folder):
            pathlib.Path(self.destination_folder).mkdir(parents=True)

        logging.basicConfig(level=logging.INFO)
        dropbox_logger = logging.getLogger("dropbox")
        dropbox_logger.setLevel(logging.WARNING)
        requests_logger = logging.getLogger("requests")
        requests_logger.setLevel(logging.WARNING)

        self.get_entires()
        self.make_folders()
        self.download_files()

    def get_entires(self):
        if self.reuse_entries and os.path.exists("all_entries"):
            with open("all_entries", "rb") as f:
                all_entries = pickle.load(f)
        else:
            logging.info("Start to fetch list of entries.")
            list_content = self.dbx.files_list_folder("", recursive = True)
            all_entries = list_content.entries
            logging.info("Fetched {} entries".format(len(all_entries)))
            while list_content.has_more:
                list_content = self.dbx.files_list_folder_continue(list_content.cursor)
                logging.info("Fetched {} entries".format(len(list_content.entries)))
                all_entries.extend(list_content.entries)
            with open("all_entries", "wb") as f:
                pickle.dump(all_entries, f)

        self.all_files = [x for x in all_entries if isinstance(x, dropbox.files.FileMetadata)]
        self.all_folders = [x for x in all_entries if isinstance(x, dropbox.files.FolderMetadata)]
        print("Discovered {} files".format(len(self.all_files)))

    def make_folders(self):
        os.chdir(self.destination_folder)
        self.all_folders.sort(key=lambda folder: folder.path_lower.count("/"))
        for folder in self.all_folders:
            levels = folder.path_lower.count("/") - 1
            path_l = folder.path_lower
            list_path_l = path_l.split("/")
            list_path_l.pop(0)
            actual_path = "."
            while levels:
                t = list_path_l.pop(0)
                for i in os.listdir(actual_path):
                    if i.lower() == t:
                        actual_path += "/" + i
                levels -= 1
            os.mkdir(actual_path + "/" + folder.name)

    def download_one_file(self, file):
        levels = file.path_lower.count("/") - 1
        path_l = file.path_lower
        list_path_l = path_l.split("/")
        list_path_l.pop(0)
        actual_path = "."
        while levels:
            t = list_path_l.pop(0)
            for i in os.listdir(actual_path):
                if i.lower() == t:
                    actual_path += "/" + i
            levels -= 1
        try:
            self.dbx.files_download_to_file(actual_path + "/" + file.name, file.path_lower)
        except dropbox.exceptions.ApiError as e:
            logging.error("Error when downloading {}".format(file.path_lower))
            logging.error(e)
        self.progress += 1/len(self.all_files)
        logging.info("Current progress: {}%".format(self.progress*100))
        if self.progress - self.printed_progress >= 0.01:
            self.printed_progress += 0.01
            logging.info("Progress: {}%".format(self.printed_progress*100))

    def download_files(self):
        self.progress = 0
        self.printed_progress = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.download_one_file, self.all_files)
        logging.info("Finished.")

# DropboxOfflineBackup()