import unittest

import os

from parsers import Parsers, ParserException


class ParsersTest(unittest.TestCase):
    def setUp(self):
        self.cwd = os.path.dirname(os.path.realpath(__file__))

    def test_typed_value(self):
        self.assertEqual(Parsers.typed_value("1234"), 1234)
        self.assertEqual(Parsers.typed_value("12.34"), 12.34)
        self.assertEqual(Parsers.typed_value("True"), True)
        self.assertEqual(Parsers.typed_value("false"), False)
        self.assertEqual(Parsers.typed_value("yes"), True)
        self.assertEqual(Parsers.typed_value("yEs"), True)
        self.assertEqual(Parsers.typed_value("tRue"), True)
        self.assertEqual(Parsers.typed_value('{"key" : "value"}'), {"key": "value"})
        self.assertEqual(Parsers.typed_value('["value1", "value2"]'), ["value1", "value2"])

    def test_line_parser(self):
        pars = Parsers()
        test_root = dict()
        pars.parse_line(test_root, "test_int = 1234")
        self.assertEqual(test_root["test_int"], 1234)
        pars.parse_line(test_root, "test_float = 12.34")
        self.assertEqual(test_root["test_float"], 12.34)

    def test_dict_parser(self):
        pars = Parsers()
        test_root = dict()
        # stop if raw ends
        raw = [
            "@dict test_dict",
            "  t_int = 1234",
            "    t_float = 12.34",
            " t_yes = yEs",
            "     t_false = faLse",
            "  t_string = string"
        ]
        pars.parse_dict_entry(test_root, raw)
        self.assertEqual(test_root["test_dict"]["t_int"], 1234)
        self.assertEqual(test_root["test_dict"]["t_float"], 12.34)
        self.assertEqual(test_root["test_dict"]["t_yes"], True)
        self.assertEqual(test_root["test_dict"]["t_false"], False)
        self.assertEqual(test_root["test_dict"]["t_string"], "string")

        # stop on next upper key
        raw = [
            "@dict test_dict",
            "  t_int = 1234",
            "    t_float = 12.34",
            " t_yes = yEs",
            "     t_false = faLse",
            "  t_string = string",
            "key_error = raised"
        ]

        def get_error_key(dic, key):
            return dic[key]

        pars.parse_dict_entry(test_root, raw)
        self.assertEqual(test_root["test_dict"]["t_int"], 1234)
        self.assertEqual(test_root["test_dict"]["t_float"], 12.34)
        self.assertEqual(test_root["test_dict"]["t_yes"], True)
        self.assertEqual(test_root["test_dict"]["t_false"], False)
        self.assertEqual(test_root["test_dict"]["t_string"], "string")
        self.assertRaises(KeyError, get_error_key, test_root["test_dict"], "key_error")

    def test_list_parser(self):
        pars = Parsers()
        test_root = dict()
        # stop if raw ends
        raw = [
            "@dict test_dict",
            "  1234",
            "    12.34",
            " yEs",
            "     faLse",
            "  string"
        ]
        pars.parse_list_entry(test_root, raw)
        self.assertEqual(test_root["test_dict"][0], 1234)
        self.assertEqual(test_root["test_dict"][1], 12.34)
        self.assertEqual(test_root["test_dict"][2], True)
        self.assertEqual(test_root["test_dict"][3], False)
        self.assertEqual(test_root["test_dict"][4], "string")

        # stop on next upper key
        raw = [
            "@dict test_dict",
            "  1234",
            "    12.34",
            " yEs",
            "     faLse",
            "  string",
            "key_error = raised"
        ]

        def get_error_key(dic, idx):
            return dic[idx]

        pars = Parsers()
        pars.parse_list_entry(test_root, raw)
        self.assertEqual(test_root["test_dict"][0], 1234)
        self.assertEqual(test_root["test_dict"][1], 12.34)
        self.assertEqual(test_root["test_dict"][2], True)
        self.assertEqual(test_root["test_dict"][3], False)
        self.assertEqual(test_root["test_dict"][4], "string")
        self.assertRaises(IndexError, get_error_key, test_root["test_dict"], 5)

    def test_json_section_parse_pass(self):
        pars = Parsers()
        test_root = dict()
        raw = [
            '  { "t_int": 1234,        ',
            '    "t_obj": {            ',
            '        "t_float": 12.34, ',
            '         "t_true": true   ',
            '     },                   ',
            '     "t_false": false,    ',
            '     "t_string": "string" ',
            '   }'
        ]
        test_root["json_pass"] = pars.parse_json_section(raw, "json_pass")

        self.assertEqual(
            test_root["json_pass"],
            dict(
                t_int=1234,
                t_obj=dict(
                    t_float=12.34,
                    t_true=True,
                ),
                t_false=False,
                t_string="string"
            )
        )

    def test_json_section_fail_silent(self):
        pars = Parsers(silent=True)
        raw = [
            '@json json_fail           ',
            '  { no__quotes: 1234,     ',
            '    "t_obj": {            ',
            '        "t_float": 12.34, ',
            '         "t_true": true   ',
            '     },                   ',
            '     "t_false": false,    ',
            '     "t_string": "string" ',
            '   }'
        ]
        self.assertEqual(pars.parse_json_section(raw, "json_fail"), {})
        self.assertEqual(pars.warnings[0], 'Parser error. Json parse error in "json_fail" section.')
        self.assertEqual(len(pars.warnings), 1)

    def test_json_section_fail_raise(self):
        pars = Parsers()
        raw = [
            '@json json_fail           ',
            '  { no__quotes: 1234,     ',
            '    "t_obj": {            ',
            '        "t_float": 12.34, ',
            '         "t_true": true   ',
            '     },                   ',
            '     "t_false": false,    ',
            '     "t_string": "string" ',
            '   }'
        ]
        with self.assertRaises(ParserException) as cm:
            pars.parse_json_section(raw, "json_fail")
        self.assertEqual(cm.exception.message, "Parser exception.Json parse error in \"json_fail\" section.")

    def test_json_parser_pass(self):
        pars = Parsers()
        test_root = dict()
        raw = [
            '@json json_pass           ',
            '  { "t_int": 1234,        ',
            '    "t_obj": {            ',
            '        "t_float": 12.34, ',
            '         "t_true": true   ',
            '     },                   ',
            '     "t_false": false,    ',
            '     "t_string": "string" ',
            '   }'
        ]
        pars.parse_json_entry(test_root, raw)
        self.assertEqual(
            test_root["json_pass"],
            dict(
                t_int=1234,
                t_obj=dict(
                    t_float=12.34,
                    t_true=True,
                ),
                t_false=False,
                t_string="string"
            )
        )

    def test_json_parser_fail_silent(self):
        pars = Parsers(silent=True)
        test_root = dict()
        raw = [
            '@json test_json           ',
            '  { no__quotes: 1234,        ',
            '    "t_obj": {            ',
            '        "t_float": 12.34, ',
            '         "t_true": true   ',
            '     },                   ',
            '     "t_false": false,    ',
            '     "t_string": "string" ',
            '   }'
        ]
        pars.parse_json_entry(test_root, raw)
        self.assertEqual(test_root["test_json"], {})
        self.assertEqual(pars.warnings[0], 'Parser error. Json entry parse error for entry: test_json.')
        self.assertEqual(len(pars.warnings), 1)

    def test_json_parser_fail_raise(self):
        pars = Parsers()
        test_root = dict()
        raw = [
            '@json test_json           ',
            '  { no__quotes: 1234,        ',
            '    "t_obj": {            ',
            '        "t_float": 12.34, ',
            '         "t_true": true   ',
            '     },                   ',
            '     "t_false": false,    ',
            '     "t_string": "string" ',
            '   }'
        ]
        with self.assertRaises(ParserException) as cm:
            pars.parse_json_entry(test_root, raw)
        self.assertEqual(cm.exception.message, "Parser exception.Json entry parse error for entry: test_json.")

    def test_symlink_list(self):
        raw = [
            "source_root/dir1 > dest_root/dir1",
            "source_root/dir2/dir21 > dest_root/dir2/dir21",
            "source_root/dir3 > dest_root/dir3"
        ]
        parsed = Parsers.parse_symlink_list(raw)
        self.assertEqual(parsed,
                         [
                             {'dest': 'dest_root/dir1', 'source': 'source_root/dir1'},
                             {'dest': 'dest_root/dir2/dir21', 'source': 'source_root/dir2/dir21'},
                             {'dest': 'dest_root/dir3', 'source': 'source_root/dir3'}
                         ])
