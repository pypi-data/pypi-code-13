from __future__ import print_function
from datetime import datetime, timedelta
from os.path import expanduser, join, isfile
import ConfigParser
import json

from elasticsearch import Elasticsearch, ElasticsearchException


class MongoAuditUploader(object):
    CONFIG_PATH = '/etc/default/mongodb-audit-uploader'

    def setup(self):
        """

        :return:
        """
        if not isfile(self.CONFIG_PATH):
            config_file = open(self.CONFIG_PATH, 'w')
            config = ConfigParser.SafeConfigParser()
            config.set(ConfigParser.DEFAULTSECT, 'audit_log_location', join(expanduser('~'), 'audit.json'))
            config.write(config_file)
            config_file.close()

    def load_config(self):
        """

        :return:
        """
        if self.config_path == self.CONFIG_PATH:
            parser = ConfigParser.SafeConfigParser()
            parser.read(self.CONFIG_PATH)
            self.days = int(parser.get(ConfigParser.DEFAULTSECT, 'days'))
            self.start_date = self.today - timedelta(days=self.days)
            self.structure['start_date'] = str(self.start_date)
            self.elasticsearch_host = parser.get(ConfigParser.DEFAULTSECT, 'elasticsearch_host')
            self.elasticsearch_port = parser.get(ConfigParser.DEFAULTSECT, 'elasticsearch_port')
            self.audit_log_location = parser.get(ConfigParser.DEFAULTSECT, 'audit_log_location')
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
                    user = entry.get("users")[0].get("user")
                    action = entry.get('atype')
                    if action == "authenticate" and entry.get('result') != 0:
                        action = 'INVALID authenticate'
                    timestamp = datetime.utcfromtimestamp(int(entry.get('ts').get('$date').get('$numberLong')) / 1000.0)
                    if (self.today - timestamp).days < int(self.days):
                        # check to see if the user is already in the structure
                        if user in self.structure['users'].keys():
                            # check to see if the action is registered for the user
                            if action in self.structure['users'][user].keys():
                                self.structure['users'][user][action] += 1
                            else:
                                self.structure['users'][user][action] = 1
                        else:
                            self.structure['users'][user] = {action: 1}
                    else:
                        continue

    def upload(self):
        """

        :return:
        """
        #create index
        es = Elasticsearch([{'host': self.elasticsearch_host, 'port': self.elasticsearch_port}])
        index = 'mongodb-audit-{}-{}-{}'.format(self.today.month, self.today.day, self.today.year)
        for user in self.structure['users']:
            try:
                es.index(index=index, doc_type='mongodb-audit', \
                         body={'user': user, 'actions': self.structure['users'][user], 'timestamp': str(self.today)},
                         timestamp=self.today)
            except ElasticsearchException as msg:
                print(msg)


    def __init__(self, config_path=CONFIG_PATH):
        self.config_path = config_path
        self.config = None
        self.days = 0
        self.elasticsearch_host = ""
        self.elasticsearch_port = ""
        self.audit_log_location = ""
        self.today = datetime.utcnow()
        self.start_date = None
        self.structure = {'users': {}}
        self.setup()
        self.load_config()
        self.parse_file()
        self.upload()
