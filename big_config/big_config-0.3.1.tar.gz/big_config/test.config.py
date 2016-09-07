import logging
import unittest

import os
from testfixtures import LogCapture

from config import Config, ConfigException


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.cwd = os.path.dirname(os.path.realpath(__file__))
        self.fail_exists_file = os.path.join(self.cwd, "fixtures", "test_exists_fail.conf")
        self.fail_read_file = os.path.join(self.cwd, "fixtures", "test_read_fail.conf")
        self.fail_content_file = os.path.join(self.cwd, "fixtures", "test_content_fail.conf")
        self.fail_json_section_file = os.path.join(self.cwd, "fixtures", "test_json_section_fail.conf")
        self.pass_schema_test = os.path.join(self.cwd, "fixtures", "test_schema_pass.conf")
        with open(self.fail_read_file, "w+") as fh:
            fh.write(self.fail_read_file)
        os.chmod(self.fail_read_file, 0o300)

    def tearDown(self):
        if os.path.isfile(self.fail_read_file):
            os.remove(self.fail_read_file)

    def test_pre_parse_pass(self):
        test_str = """
            # test config file
              # test comment strip function

            this  be left out

            [standard_section]

                # inner comment
                standard body line1
                standard body line2

                standard body line3

                [@DIRTREE test_paths]

                dirtree body line1

                # inner comment
                dirtree body line2
                dirtree body line3
        """
        cfg = Config()
        raw_data = cfg.pre_parse(test_str)
        self.assertEqual(raw_data[0]["name"], "standard_section")
        self.assertEqual(raw_data[0]["type"], 0)
        self.assertEqual(raw_data[0]["body"], [
            "                standard body line1",
            "                standard body line2",
            "                standard body line3"
        ])
        self.assertEqual(raw_data[1]["name"], "test_paths")
        self.assertEqual(raw_data[1]["type"], 1)
        self.assertEqual(raw_data[1]["body"], [
            "                dirtree body line1",
            "                dirtree body line2",
            "                dirtree body line3"
        ])

    def test_pre_parse_fail_section_silent(self):
        test_str = """
            [standard_section]
                standard body line1
                standard body line2
                standard body line3

            [@FAIL fail_section]
                fail body line1
                fail body line2
        """
        cfg = Config(silent=True)
        raw_data = cfg.pre_parse(test_str)
        self.assertEqual(raw_data[0]["name"], "standard_section")
        self.assertEqual(raw_data[0]["type"], 0)
        self.assertEqual(raw_data[0]["body"], [
            "                standard body line1",
            "                standard body line2",
            "                standard body line3"
        ])
        self.assertEqual(len(raw_data), 1)
        self.assertEqual(cfg.warnings()[0], "Config Exception. Key error raised in section type: FAIL")
        self.assertEqual(len(cfg.warnings()), 1)

    def test_pre_parse_fail_section_raise(self):
        test_str = """
            [standard_section]
                standard body line1
                standard body line2
                standard body line3

            [@FAIL fail_section]
                fail body line1
                fail body line2
        """
        with LogCapture() as l:
            logger = logging.getLogger()
            cfg = Config(logger=logger)
            self.assertRaises(ConfigException, cfg.pre_parse, test_str)
            self.assertTrue("Key error raised in section type: fail_section", l.records[0].msg)
            self.assertTrue(len(l.records) == 1)

    def test_read_config_fail_raise(self):
        with LogCapture() as l:
            logger = logging.getLogger()
            cfg = Config(logger=logger)
            self.assertRaises(
                ConfigException,
                cfg.read_config,
                os.path.join(self.cwd, "fixtures", self.fail_exists_file)
            )
            self.assertEqual(len(l.records), 1)
            self.assertTrue(self.fail_exists_file in l.records[0].msg)

    def test_read_config_file_fail_silent(self):
        cfg = Config(silent=True)
        self.assertEqual(cfg.read_config(self.fail_exists_file), "")
        self.assertEqual(
            cfg.warnings()[0],
            "Config error. " + self.fail_exists_file + " missing configuration file."
        )
        self.assertEqual(len(cfg.warnings()), 1)

    def test_read_config_file_fail_raise(self):
        with LogCapture() as l:
            logger = logging.getLogger()
            self.assertRaises(ConfigException, Config, os.path.join(self.cwd, "fixtures", self.fail_read_file), logger)
            self.assertEqual(len(l.records), 1)
            self.assertTrue(self.fail_read_file in l.records[0].msg)
            self.assertTrue("Permission denied" in l.records[0].msg)

    def test_read_config_content_fail_silent(self):
        cfg = Config(silent=True)
        self.assertEqual(cfg.read_config(self.fail_read_file), "")
        self.assertEqual(
            cfg.warnings()[0],
            "Configuration error for file: " + self.fail_read_file + " -  Permission denied."
        )
        self.assertEqual(len(cfg.warnings()), 1)

    def test_content_config_fail_raise(self):
        with LogCapture() as l:
            logger = logging.getLogger()
            self.assertRaises(ConfigException, Config, self.fail_content_file, logger)
            self.assertEqual(len(l.records), 1)
            self.assertTrue(self.fail_content_file + " is empty" in l.records[0].msg)

    def test_content_config_no_output_fail_raise(self):
        test_str = \
            """
                no section line1
                no section line2
            """
        with LogCapture() as l:
            logger = logging.getLogger()
            cfg = Config(logger=logger)
            self.assertRaises(ConfigException, cfg.pre_parse, test_str)
            self.assertTrue("Config error. Could not parse file content. Got empty dict", l.records[0].msg)
            self.assertTrue(len(l.records) == 1)

    def test_json_section_fail_raise(self):
        with LogCapture() as l:
            logger = logging.getLogger()
            self.assertRaises(ConfigException, Config, self.fail_json_section_file, logger)
            self.assertEqual(len(l.records), 1)
            self.assertTrue('Parser exception.Json parse error in "json_fail" section.' in l.records[0].msg)

    def test_json_section_fail_silent(self):
        cfg = Config(self.fail_json_section_file, silent=True)
        self.assertEqual(cfg, {
            'json_fail': {},
            'standard_section1': {
                'sec1_key1': 'sec1_value1',
                'sec1_key3': 'sec1_value3',
                'sec1_key2': 'sec1_value2'
            },
            'standard_section2': {
                'sec2_key1': 'sec2_value1',
                'sec2_key2': 'sec2_value2',
                'sec2_key3': 'sec2_value3'
            }
        })
        self.assertEqual(
            cfg.warnings()[0],
            "Parser error. Json parse error in \"json_fail\" section."
        )
        self.assertEqual(len(cfg.warnings()), 1)

    def test_config_data_pass(self):
        cfg = Config(os.path.join(self.cwd, "fixtures", "test1.conf"))
        self.assertEqual(cfg["standard_section"], dict(
            test_int=1234,
            test_float=12.34,
            test_bool=True,
            test_string="string",
            dict_entry=dict(
                key1="value1",
                key2="value2"
            ),
            test_key="test_value",
            list_entry=["v1", 1234, True],
            test_json_entry={u'key21': u'value21', u'ke1': {u'key12': u'value12', u'key11': u'value11'}},
            test_json_list=[u'item1', u'item2', {u'key1': u'value1'}],
            test_json_line={u'key21': u'value21', u'ke1': {u'key12': u'value12', u'key11': u'value11'}}
        ))
        self.assertEqual(cfg["test_json_section"],
                         {u'key21': u'value21', u'ke1': {u'key12': u'value12', u'key11': u'value11'}})
        self.assertEqual(cfg["test_paths"],
                         [
                             'dir1',
                             'dir1/dir11',
                             'dir1/dir12',
                             'dir1/dir12/dir121',
                             'dir2',
                             'dir2/dir21',
                             'dir2/dir22',
                             'dir2/dir23'
                         ])
        self.assertEqual(cfg["sym_list"],
                         [
                             {'dest': 'dest_root/dir1', 'source': 'source_root/dir1'},
                             {'dest': 'dest_root/dir2/dir21', 'source': 'source_root/dir2/dir21'},
                             {'dest': 'dest_root/dir3', 'source': 'source_root/dir3'}
                         ])

    def test_schema_pass(self):
        conf_schema = {
            "standard_section": {
                "type": "dict",
                "schema": {
                    "test_int": {
                        "type": "integer",
                        "required": True
                    },
                    "test_float": {
                        "type": "float",
                        "required": True
                    },
                    "test_bool": {
                        "type": "boolean",
                        "required": True
                    },
                    "test_string": {
                        "type": "string",
                        "required": True
                    },
                    "test_dict": {
                        "type": "dict",
                        "schema": {
                            "key1": {
                                "type": "string",
                                "required": True
                            },
                            "key2": {
                                "type": "string",
                                "required": True
                            }
                        }
                    },
                    "test_list": {
                        "type": "list",
                        "schema": {
                            "allow_unknown": True
                        }
                    }
                }
            }
        }
        cfg = Config(schema=conf_schema)
        self.assertEqual(
            cfg.initialize(self.pass_schema_test),
            {
                'standard_section': {
                    'test_dict': {
                        'key2': 'value2',
                        'key1': 'value1'
                    },
                    'test_bool': True,
                    'test_list': ['v1', 1234, True],
                    'test_float': 12.34,
                    'test_int': 1234,
                    'test_string': 'string'
                }
            }
        )
        self.assertEqual(len(cfg.warnings()), 0)

    def test_schema_fail_raise(self):
        conf_schema = {
            "standard_section": {
                "type": "dict",
                "schema": {
                    "test_int": {
                        "type": "string",  # this will fail
                        "required": True
                    },
                    "test_float": {
                        "type": "float",
                        "required": True
                    },
                    "test_bool": {
                        "type": "boolean",
                        "required": True
                    },
                    "test_string": {
                        "type": "string",
                        "required": True
                    },
                    "test_dict": {
                        "type": "dict",
                        "schema": {
                            "key1": {
                                "type": "string",
                                "required": True
                            },
                            "key2": {
                                "type": "string",
                                "required": True
                            }
                        }
                    },
                    "test_list": {  # this will fail too
                        "type": "integer",
                    }
                }
            }
        }
        with LogCapture() as l:
            logger = logging.getLogger()
            cfg = Config(schema=conf_schema, logger=logger)
            self.assertRaises(ConfigException, cfg.initialize, self.pass_schema_test)
            self.assertEqual(len(l.records), 1)
            self.assertEqual(
                'Configuration validation error(s): \n{\n   "standard_section": ' +
                '{\n      "test_int": "must be of string type", ' +
                '\n      "test_list": "must be of integer type"\n   }\n}',
                l.records[0].msg
            )

    def test_schema_fail_silent(self):
        conf_schema = {
            "standard_section": {
                "type": "dict",
                "schema": {
                    "test_int": {
                        "type": "string",  # this will fail
                        "required": True
                    },
                    "test_float": {
                        "type": "float",
                        "required": True
                    },
                    "test_bool": {
                        "type": "boolean",
                        "required": True
                    },
                    "test_string": {
                        "type": "string",
                        "required": True
                    },
                    "test_dict": {
                        "type": "dict",
                        "schema": {
                            "key1": {
                                "type": "string",
                                "required": True
                            },
                            "key2": {
                                "type": "string",
                                "required": True
                            }
                        }
                    },
                    "test_list": {  # this will fail too
                        "type": "integer",
                    }
                }
            }
        }
        cfg = Config(schema=conf_schema, silent=True)
        self.assertEqual(cfg.initialize(self.pass_schema_test), {})
        self.assertEqual(len(cfg.warnings()), 1)
        self.assertEqual(
            'Configuration validation error(s): \n{\n   "standard_section": ' +
            '{\n      "test_int": "must be of string type", ' +
            '\n      "test_list": "must be of integer type"\n   }\n}',
            cfg.warnings()[0]
        )
