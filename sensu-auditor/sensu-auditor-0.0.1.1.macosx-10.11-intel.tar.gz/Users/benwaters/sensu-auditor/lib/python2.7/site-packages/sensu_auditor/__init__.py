from __future__ import print_function
from datetime import datetime, timedelta
from configparser import NoOptionError, DEFAULTSECT, SafeConfigParser
import json
from os.path import expanduser, isfile, isdir, join
from os import listdir
import gzip
import logging


from defaults import CONFIG_PATH, SENSU_LOG_FOLDER, LOG_LOCATION, LOG_TYPES, \
    MESSAGES, DEFAULT_CONFIG_FIELDS, DEFAULT_SECTIONS
from unhealthy import UnhealthyList, UnhealthyEntry
from raw import RawReportableEntry, RawReportableList
from report import SensuReport

from dateutil.parser import parse
from elasticsearch import Elasticsearch, ElasticsearchException


class SensuAuditor(object):

    def logger_init(self):
        """

        :return:
        """
        # TO DO: in the future allow using somethign other to console for logger
        self.logger = logging.getLogger(__name__)
        # TO DO: allow other than debug logger
        self.logger.setLevel(logging.DEBUG)
        sh = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        sh.setFormatter(formatter)
        self.logger.addHandler(sh)

    def setup(self):
        self.logger_init()
        self.load_config()

    def load_config(self):
        """

        :return:
        """
        config = SafeConfigParser()
        config.read(self.config_path)
        # set defaults
        self.days = int(config.get(DEFAULTSECT, 'days'))
        self.start_date = self.today - timedelta(days=self.days)
        if config.has_section(DEFAULT_SECTIONS['group']):
            # subtract defaults from groups list
            options = list(set(config.options(DEFAULT_SECTIONS['group'])) - set(DEFAULT_CONFIG_FIELDS.keys()))
            for option in options:
                checks = [x.strip() for x in config.get(DEFAULT_SECTIONS['group'], option).split(',')]
                # master list of checks
                self.checks.extend(checks)
                self.report.content[option] = SensuAuditor.generate_format(checks)
        if config.has_section(DEFAULT_SECTIONS['user']):
            self.logger.info('has user config')
            if config.has_option(DEFAULT_SECTIONS['user'], 'days'):
                self.days = int(config.get(DEFAULT_SECTIONS['user'], 'days'))
                self.start_date = self.today - timedelta(days=self.days)
            if config.has_option(DEFAULT_SECTIONS['user'], 'elasticsearch_host'):
                self.logger.info('overwrote es host')
                self.elasticsearch_host = config.get(DEFAULT_SECTIONS['user'], 'elasticsearch_host')
                self.elasticsearch_port = config.get(DEFAULT_SECTIONS['user'], 'elasticsearch_port')
            try:
                log_location = expanduser(config.get(DEFAULT_SECTIONS['user'], LOG_LOCATION))
                if isfile(log_location):
                    # single file
                    self.parse_log_file(log_location)
                elif isdir(log_location):
                    # directory glob
                    self.parse_log_directory(log_location)
                else:
                    self.logger.error('bad format')
            except NoOptionError:
                self.logger.info('user did not override log location')

    @staticmethod
    def parse_timestamp(timestamp):
        """

        :param timestamp:
        :return:
        """
        return parse(timestamp)

    @staticmethod
    def generate_format(checks):
        """

        :param checks:
        :return:
        """
        return {x: {'dt': 0.0} for x in checks}

    def parse_gzip_file(self, log_location):
        """

        :param log_location:
        :return:
        """
        with gzip.open(log_location, 'r+') as log_file:
            for entry in log_file:
                json_message = json.loads(entry)
                message = json_message.get('message')
                timestamp = parse(json_message.get('timestamp'), ignoretz=True)
                if message == MESSAGES['PUBLISHED_MESSAGE']:
                    if (self.today - timestamp).days < int(self.days):
                        check_name = json_message.get('payload').get('check').get('name')
                        status = json_message.get('payload').get('check').get('status')
                        if status != 0 and check_name in self.checks \
                                and check_name not in self.unhealthy_checks.names():
                            self.unhealthy_checks.append(UnhealthyEntry(check_name=check_name, start_time=timestamp))
                        elif status == 0 and check_name in self.checks and check_name in self.unhealthy_checks.names():
                            done = self.unhealthy_checks.pop(self.unhealthy_checks.get_by_name(check_name))
                            entry = RawReportableEntry(check_name=done.check_name,
                                                       start_time=done.start_time,
                                                       end_time=timestamp,
                                                       category=self.report.get_group_by_check(check_name))
                            self.raw_reportable.append(entry)
        self.report.add_raw_entries(self.raw_reportable)

    def parse_regular_file(self, log_location):
        """

        :param log_location:
        :return:
        """
        with open(log_location, 'r+') as log_file:
            for entry in log_file:
                json_message = json.loads(entry)
                message = json_message.get('message')
                timestamp = parse(json_message.get('timestamp'), ignoretz=True)
                if message == MESSAGES['PUBLISHED_MESSAGE']:
                    if (self.today - timestamp).days < int(self.days):
                        check_name = json_message.get('payload').get('check').get('name')
                        status = json_message.get('payload').get('check').get('status')
                        if status != 0 and check_name in self.checks \
                                and check_name not in self.unhealthy_checks.names():
                            self.unhealthy_checks.append(UnhealthyEntry(check_name=check_name, start_time=timestamp))
                        elif status == 0 and check_name in self.checks \
                                and check_name in self.unhealthy_checks.names():
                            done = self.unhealthy_checks.pop(self.unhealthy_checks.get_by_name(check_name))
                            self.raw_reportable.append(RawReportableEntry(done.check_name, done.start_time, timestamp))

    def parse_log_file(self, log_location):
        """

        :param log_location:
        :return:
        """
        if log_location.endswith('.gz'):
            self.parse_gzip_file(log_location)
        else:
            self.parse_regular_file(log_location)

    def parse_log_directory(self, log_location):
        """

        :param log_location:
        :return:
        """
        filenames = []
        for filename in listdir(log_location):
            filenames.extend([join(log_location, filename) for x in LOG_TYPES if x in filename])
        for name in filenames:
            self.parse_log_file(name)

    def upload(self):
        """

        :return:
        """
        # check settings to see if elasticsearch stuff was overwritten
        if self.elasticsearch_host is not None and self.elasticsearch_port is not None:
            es = Elasticsearch([{'host': str(self.elasticsearch_host), 'port': int(self.elasticsearch_port)}])
            self.logger.info('using custom elastic search settings')
        else:
            es = Elasticsearch()
        # standard es index
        index = 'sensu-audit-{}-{}-{}'.format(self.today.year, self.today.month, self.today.day)
        try:
            es.index(index=index, doc_type='sensu-audit',
                     body={'hostname': self.report.hostname,
                           'total_downtime': self.report.total_downtime,
                           'timestamp': str(self.today.strftime('%Y-%m-%dT%H:%M:%S.%fZ')),
                           'affected': self.report.content},
                     timestamp=self.today)
        except ElasticsearchException as msg:
            self.logger.error(msg)

    def __init__(self, config_path=CONFIG_PATH):
        """

        :param config_path:
        """
        self.logger = None
        self.checks = []
        self.config_path = config_path
        self.elasticsearch_host = None
        self.elasticsearch_port = None
        self.audit_log_location = ""
        self.today = datetime.utcnow()
        self.report = SensuReport(downtime=0)
        self.unhealthy_checks = UnhealthyList()
        self.raw_reportable = RawReportableList()
        self.start_date = None
        self.days = 0
        self.total_downtime = 0
        self.setup()
        self.upload()
