import configparser
import os
import logging
import platform

class DropboxOfflineBackupConfig:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.optionxform = str
        if platform.system() == "Linux":
            self.config_file = "/etc/dropboxofflinebackup.conf"
            if os.path.exists(self.config_file):
                self.config.read(self.config_file)
                try:
                    assert type(self.config['DropboxBackup']['AccessToken']).__name__ == 'str'
                    assert self.config['DropboxBackup']['AccessToken'] != "CHANGE_THIS_TO_YOUR_ACCESS_TOKEN"
                except AssertionError as e:
                    logging.error(e)
                    logging.error("Access token not valid.")
            else:
                self.config['DropboxBackup'] = {
                    "BackupDestinationPath" : os.path.expanduser('~')+"/DropboxBackup",
                    "ConcurrentThreads" : 5,
                    "AccessToken": "CHANGE_THIS_TO_YOUR_ACCESS_TOKEN"
                }
                with open(self.config_file, 'w') as configfile:
                    self.config.write(configfile)
                print("Generated default config file at {}".format(self.config_file))
                print("Please modify the config file and get the access token according to the manual.")
                exit()
        else:
            logging.error("Current only support Linux.")
            exit()
