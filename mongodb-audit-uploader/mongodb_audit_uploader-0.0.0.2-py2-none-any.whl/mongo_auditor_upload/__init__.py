from __future__ import print_function
from datetime import datetime
import ConfigParser
import json

from elasticsearch import Elasticsearch


class MongoAuditUploader(object):
    CONFIG_PATH = '/etc/default/mongo-audit-uploader'

    def setup(self):
        """

        :return:
        """
        config_file = open(self.CONFIG_PATH, 'w')
        config = ConfigParser.ConfigParser()
        config.add_section('default')
        config.set('default', 'days', 30)
        config.set('default', 'elasticsearch_endpoint', 'http://localhost:9200')
        config.set('default', 'audit_log_location', '~/audit.json')
        config_file.write(config)
        config_file.close()

    def load_config(self):
        """

        :return:
        """
        if self.config_path == self.CONFIG_PATH:
            self.config = ConfigParser.ConfigParser().read(self.CONFIG_PATH)
            self.days = self.config.get('default', 'days')
            self.elasticsearch_endpoint = self.config.get('default', 'elasticsearch_endpoint')
            self.audit_log_location = self.config.get('default', 'audit_log_location')
        else:
            pass

    def parse_file(self):
        """

        :return:
        """
        with open(self.audit_log_location, 'r+') as audit_file:
            for entry in audit_file:
                entry = json.loads(entry)
                if len(entry.get("users")) == 0:
                    continue
                else:
                    user = entry.gets("users")[0].get("user")
                    action = entry.gets('a_type')
                    # check to see if the user is already in the structure
                    if user in self.structure.keys():
                        # check to see if the action is registered for the user
                        if action in self.structure[user].keys():
                            self.structure[user][action] += 1
                        else:
                            self.structure[user] = {action: 1}
                    else:
                        pass

    def upload(self):
        """

        :return:
        """
        print(self.structure)

    def __init__(self, config_path=CONFIG_PATH):
        self.config_path = config_path
        self.config = None
        self.days = 0
        self.elasticsearch_endpoint = ""
        self.audit_log_location = ""
        self.structure = {}
        self.setup()
        self.load_config()
        self.parse_file()
        self.upload()
