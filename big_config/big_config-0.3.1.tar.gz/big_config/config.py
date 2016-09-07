import json

import os
from cerberus import Validator

from constants import *
from parsers import Parsers, ParserException


class ConfigException(Exception):
    def __init__(self, message):
        self.message = message
        Exception.__init__(self, self.message)


class Config(dict):
    def __init__(self, config_file="", logger=None,
                 silent=False, schema=None):
        super(Config, self).__init__(self)
        self.__warnings = []
        self.__logger = logger
        self.__silent = silent
        self.__schema = schema
        self.__parsers = Parsers(silent=silent)
        if config_file:
            self.initialize(config_file)

    def initialize(self, config_file):
        content = self.read_config(config_file)
        if content:
            raw_data = self.pre_parse(content)
            if len(raw_data):
                data = self.parse(raw_data)
                if len(data):
                    if self.__schema:
                        if not self.validate(data):
                            return {}
                    self.update(data)
                    return self
        return {}

    def log(self, message):
        if not self.__silent:
            if self.__logger:
                self.__logger.error(message)
            raise ConfigException(message)
        self.__warnings.append(message)

    def pre_parse(self, content):
        raw_data = []
        section_name = ""
        conf_arr = content.split("\n")
        if len(conf_arr) < 2:
            self.log("Config Exception. Corrupted or missing config file content.")
            return []
        for idx in range(0, len(conf_arr)):
            line = conf_arr[idx]
            if not line.strip() or line.strip()[0] == COMMENT_MARK:
                continue
            if line.strip()[0] == SECTION_IN and line.strip()[-1] == SECTION_OUT:
                section_name = line.strip()[1:-1]
                if section_name[0] == PARSER_SECTION:
                    bits = section_name.split(BLANK)
                    section_name = bits[1]
                    try:
                        section_type = SECTION_TYPES[bits[0][1:]]
                    except KeyError:
                        self.log("Config Exception. Key error raised in section type: %s" % bits[0][1:])
                        section_name = ""
                        continue
                else:
                    section_type = 0
                raw_data.append(dict(name=section_name, type=section_type, body=[]))
                continue
            if not section_name:
                continue
            raw_data[-1]["body"].append(line)
        if not raw_data or not len(raw_data):
            self.log("Config error. Could not parse file content. Got empty dict")
            return []
        return raw_data

    def read_config(self, config_file):

        if not os.path.isfile(config_file):
            self.log("Config error. %s missing configuration file." % config_file)
            return ""
        try:
            conf = open(config_file, "r")
            content = conf.read()
        except IOError as err:
            self.log("Configuration error for file: %s -  %s." %
                     (config_file, err.strerror or err.message))
            return ""
        if conf and not conf.closed:
            conf.close()
        if not content:
            self.log("Configuration error. Configuration file %s is empty." % config_file)
        return content

    def parse(self, raw_data):
        output = dict()
        for item in raw_data:
            try:
                if item["type"] == 1:
                    output[item["name"]] = self.__parsers.parse_dir_list(item["body"])
                    continue

                if item["type"] == 2:
                    output[item["name"]] = self.__parsers.parse_symlink_list(item["body"])
                    continue

                if item["type"] == 3:
                    output[item["name"]] = self.__parsers.parse_json_section(item["body"], item["name"])
                    continue

                output[item["name"]] = self.__parsers.parse(item["body"])
            except ParserException as err:
                self.log(err.message)
            self.__warnings += self.__parsers.warnings
        if not len(output):
            message = "Configuration error. Config dict is empty"
            self.log(message)
        return output

    def validate(self, conf):
        validator = Validator()
        if validator(conf, self.__schema):
            return True
        self.log("Configuration validation error(s): \n" +
                 json.dumps(validator.errors, indent=3))
        return False

    def warnings(self):
        return self.__warnings

    def status(self):
        return dict(
            _status="OK" if len(self.__warnings) == 0 else "ERR",
            _errors=self.warnings
        )
