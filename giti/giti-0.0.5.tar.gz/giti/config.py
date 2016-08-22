import configparser
import os


class Config:
    __config = configparser.ConfigParser()
    __conf_dir = os.path.expanduser("~/.giticonf")

    def __init__(self):
        self.__config.read(self.__conf_dir)

    def get_proxy(self):
        if 'proxy' in self.__config:
            if 'address' in self.__config['proxy']:
                return self.__config['proxy']['address']

    def set_proxy(self, url):
        self.__config['proxy']['address'] = url
        self.__save()

    def __save(self):
        with open(self.__conf_dir, 'w') as configfile:
            self.__config.write(configfile)
