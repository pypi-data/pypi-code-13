import json

from big_config.path_list import PathsList
from constants import *


class ParserException(Exception):
    def __init__(self, message):
        self.message = "Parser exception." + message
        Exception.__init__(self, self.message)


class Parsers(object):
    def __init__(self, silent=False, warnings=None):
        self.silent = silent
        self.warnings = warnings if warnings else []

    @staticmethod
    def typed_value(entry):
        # is it an integer?
        try:
            return int(entry)
        except ValueError:
            pass
        # is it a float?
        try:
            return float(entry)
        except ValueError:
            pass
        # is it a boolean value ?
        if entry.lower() == "yes" or entry.lower() == "true":
            return True
        if entry.lower() == "no" or entry.lower() == "false":
            return False
        # if it's a json
        if entry[0] in ["{", "["] and entry[-1] in ["}", "]"]:
            try:
                entry = json.loads(entry)
            except (AttributeError, ValueError):
                # then it's definitely a string
                return entry
        # is a json parsed value
        return entry

    @staticmethod
    def get_indent(line):
        return len(line) - len(line.lstrip())

    def parse_line(self, root, line):
        bits = line.split(EQ)
        root[bits[0].strip()] = self.typed_value(bits[1].strip())

    def parse_dict_entry(self, root, raw):
        entry = raw[0].strip().split(BLANK)[1].strip()
        indent = self.get_indent(raw[0])
        del raw[0]
        root[entry] = dict()
        while len(raw) and self.get_indent(raw[0]) > indent:
            self.parse_line(root[entry], raw[0])
            del raw[0]

    def parse_json_entry(self, root, raw):
        entry = raw[0].strip().split(BLANK)[1].strip()
        indent = self.get_indent(raw[0])
        del raw[0]
        raw_json = ""
        while len(raw) and self.get_indent(raw[0]) > indent:
            raw_json += raw[0]
            del raw[0]
        try:
            root[entry] = json.loads(raw_json)
        except (AttributeError, ValueError):
            message = "Json entry parse error for entry: %s." % entry
            self.warnings.append("Parser error. " + message)
            if not self.silent:
                raise ParserException(message)
            root[entry] = {}

    def parse_json_section(self, raw, name):
        try:
            return json.loads("".join(raw))
        except (AttributeError, ValueError):
            message = "Json parse error in \"%s\" section." % name
            self.warnings.append("Parser error. " + message)
            if not self.silent:
                raise ParserException(message)
        return {}

    def parse_list_entry(self, root, raw):
        entry = raw[0].strip().split(BLANK)[1].strip()
        indent = self.get_indent(raw[0])
        del raw[0]
        root[entry] = []
        while len(raw) and self.get_indent(raw[0]) > indent:
            root[entry].append(self.typed_value(raw[0].strip()))
            del raw[0]

    @staticmethod
    def parse_symlink_list(raw):
        output = []
        while len(raw):
            while len(raw) and ARROW in raw[0]:
                entry = raw[0].split(ARROW)
                output.append({'source': entry[0].strip(), 'dest': entry[1].strip()})
                del raw[0]
        return output

    @staticmethod
    def parse_dir_list(raw):
        return PathsList(raw)

    def parse(self, raw):
        output = dict()
        while len(raw):
            while len(raw) and EQ in raw[0]:
                self.parse_line(output, raw[0])
                del raw[0]
            if len(raw) and DICT_ENTRY in raw[0]:
                self.parse_dict_entry(output, raw)
            if len(raw) and LIST_ENTRY in raw[0]:
                self.parse_list_entry(output, raw)
            if len(raw) and JSON_ENTRY in raw[0]:
                self.parse_json_entry(output, raw)
        return output
