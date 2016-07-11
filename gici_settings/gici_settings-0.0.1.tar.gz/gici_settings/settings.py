import json
import os

from anon import AnonObject

SETTINGS = 'settings'
LOGGING = 'logging'
JSON = ".json"
SETTINGS_FILE = SETTINGS + JSON
SETTINGS_FILE_FORMAT = SETTINGS + "-{level}" + JSON
LOGGING_FILE = LOGGING + JSON


class Settings:
    def __init__(self, base_dir):
        self.settings_dir = self.get_settings_directory(base_dir)

    def load_config(self, config_level=None):
        """
        load basic conf from settings.json and update it with settings-{level}.json if exists
        :param config_level: the level to load
        :return:
        """
        basic_config = self.get_basic_conf()

        config_level_obj = self.get_conf_by_level(level=config_level) if config_level else None
        if config_level_obj:
            basic_config.update(config_level_obj)
        return AnonObject(**basic_config)

    def get_basic_conf(self):
        return self.get_conf_by_level()

    def get_conf_by_level(self, level=None):
        config_file = self.get_config_file(level)
        config_obj = self.get_config_object(config_file)
        return config_obj

    def get_config_file(self, level=None):
        config_file_name = SETTINGS_FILE if level is None else SETTINGS_FILE_FORMAT.format(level=level)
        return os.path.join(self.settings_dir, config_file_name)

    @staticmethod
    def get_settings_directory(base_dir):
        return os.path.join(base_dir, SETTINGS)

    @staticmethod
    def get_config_object(file_path):
        if not os.path.isfile(file_path):
            print "configuration file doesn't exist at: {}".format(file_path)
            return

        with open(file_path, 'r') as f:
            conf = json.load(f)
        return conf

    @staticmethod
    def get_logging_file(settings_dir):
        return os.path.join(settings_dir, LOGGING_FILE)


