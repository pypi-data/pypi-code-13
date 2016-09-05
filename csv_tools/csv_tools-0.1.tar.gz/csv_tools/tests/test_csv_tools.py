import os
import sys
from collections import defaultdict
from os.path import dirname
from pathlib import Path
from tempfile import NamedTemporaryFile
from types import GeneratorType

import pytest
from hypothesis import (given, strategies as st)
from logbook import Logger, StreamHandler

from csv_tools import (DialectDetector,
                       SchemaEngine,
                       sniff_for_encoding,
                       integrity_check)

__author__ = "cw-andrews"


def normalized_join(*path_parts: str):
    """Take *path_parts and return a joined and normalized filepath."""

    complete_path = os.path.join(*path_parts)
    normalized_path = os.path.normpath(complete_path)

    return normalized_path


logger = Logger()
StreamHandler(sys.stdout).push_application()

W_DIR = dirname(__file__)

INV_TEST_REG = normalized_join(W_DIR, "static", "inv_test.csv")
INV_TEST_NH = normalized_join(W_DIR, "static", "inv_test_headers_none.csv")
INV_TEST_PRO = normalized_join(W_DIR, "static", "inv_test_processed.csv")
INV_TEST_PIPE = normalized_join(W_DIR, "static", "inv_test_pipe.csv")
INV_TEST_PIPE2 = normalized_join(W_DIR, "static", "maxie_price_rv_inv.csv")
INV_TEST_WH = normalized_join(W_DIR, "static", "inv_test_headers_weird.csv")
INV_TEST_TAB = normalized_join(W_DIR, "static", "inv_test_tab.csv")
INV_TEST_BAD = normalized_join(W_DIR, "static", "feed.csv")

INTEG_RET = normalized_join(W_DIR, "static", "tfi_feeds.txt")


@pytest.fixture(scope="function")
def test_file(request):
    temp_file = NamedTemporaryFile(delete=False)
    temp_filepath = temp_file.name

    def fin():
        p = Path(temp_filepath)
        if p.exists():
            p.unlink()

    request.addfinalizer(fin)
    return temp_filepath


@pytest.fixture(scope="class")
def test_instantiate_dialect_detector():
    dd = DialectDetector()
    return dd


@pytest.fixture(scope="class")
def test_instantiate_schema_engine():
    se = SchemaEngine()
    return se


@given(encoding=st.sampled_from(('utf-32', 'utf-16', 'utf-8', 'ascii',
                                 'latin-1')),
       read_file=st.sampled_from((INV_TEST_REG, INV_TEST_NH, INV_TEST_PRO,
                                  INV_TEST_PIPE, INV_TEST_WH, INV_TEST_TAB,
                                  INV_TEST_BAD)))
def test_sniff_for_encoding_diff_files(read_file, test_file, encoding):
    working_file = test_file

    valid_encodings = ("utf-32", "utf-16", "utf-8", "ascii", "latin-1",
                       "iso-8859-2", "utf-32le", "utf-16le", "utf-32be",
                       "utf-16be", "utf-8-sig")

    read_file_encoding = sniff_for_encoding(read_file)

    with open(read_file, "rt", encoding=read_file_encoding) as r, open(
            working_file, "wt", encoding=encoding, errors="replace") as w:
        for line in r.readlines():
            w.write(line)

    with Path(working_file) as p:
        assert p.exists()
        assert p.stat().st_size > 0

    determined = sniff_for_encoding(working_file)
    assert isinstance(determined, str)
    assert determined.lower() in valid_encodings


def test_sniff_for_encoding_spec_files():

    assert sniff_for_encoding(INV_TEST_NH).lower() == "utf-8"


class TestDialectDetector:

    @given(read_file=st.sampled_from((INV_TEST_REG, INV_TEST_NH, INV_TEST_PRO,
                                      INV_TEST_PIPE, INV_TEST_WH, INV_TEST_TAB,
                                      INV_TEST_BAD)),
           encoding=st.sampled_from(('utf-8', 'latin-1')))
    def test_sniff_for_dialect_diff_files(self,
                                          read_file,
                                          test_file,
                                          encoding):
        dd = test_instantiate_dialect_detector()
        working_file = test_file

        with open(read_file, "rt", encoding=encoding) as r, open(
                working_file, "wt", errors="replace") as w:
            for line in r.readlines():
                w.write(line)

        with Path(working_file) as p:
            assert p.exists()
            assert p.stat().st_size > 0

        sniffed = dd.sniff_for_dialect(working_file)
        assert sniffed.delimiter
        assert sniffed.quotechar in ('"', "'")

    def test_sniff_for_dialect_spec_files(self):
        dd = test_instantiate_dialect_detector()

        regular = dd.sniff_for_dialect(INV_TEST_REG)
        assert regular.delimiter == ","
        assert regular.quotechar == '"'

        assert dd.sniff_for_dialect(INV_TEST_PIPE).delimiter == "|"
        assert dd.sniff_for_dialect(INV_TEST_TAB).delimiter == "\t"

    @given(test_file=st.sampled_from((INV_TEST_REG, INV_TEST_NH, INV_TEST_PRO,
                                      INV_TEST_PIPE, INV_TEST_WH, INV_TEST_TAB,
                                      INV_TEST_BAD)),
           encoding=st.sampled_from(('utf-8', 'latin-1')))
    def test_sniff_for_headers_ret_list_of_str(self, test_file, encoding):
        dd = test_instantiate_dialect_detector()

        generated_headers = dd.sniff_for_headers(test_file, encoding=encoding)

        assert isinstance(generated_headers, list)
        assert len(generated_headers) > 1

        for h in generated_headers:
            assert isinstance(h, str)

    def test_sniff_for_headers_spec_files(self):
        dd = test_instantiate_dialect_detector()

        manufactured_headers = dd.sniff_for_headers(INV_TEST_NH)
        for h in manufactured_headers:
            assert h.startswith("Column")

        reg_headers = dd.sniff_for_headers(INV_TEST_REG)
        for h in reg_headers:
            assert not h.startswith("Column")

        assert dd.sniff_for_headers(INV_TEST_WH) == reg_headers

    def test_sniff_for_headers_delimiter_override(self):
        dd = test_instantiate_dialect_detector()

        headers = dd.sniff_for_headers(INV_TEST_PIPE2,
                                       delimiter_override='|')

        assert len(headers) > 1
        assert headers[0] == 'ID'
        for h in headers:
            assert '|' not in h


class TestSchemaEngine:
    @given(val=st.integers(min_value=0, max_value=255))
    def test_rounded_len_diff_vals_flight_one(self, val):
        se = test_instantiate_schema_engine()

        assert isinstance(se.rounded_len(se.text_lengths, val), int)

        n = se.rounded_len(se.text_lengths, val)
        assert n == abs(n)

        assert se.rounded_len(se.text_lengths, val) in se.text_lengths

    @given(val=st.integers(min_value=256, max_value=25000))
    def test_rounded_len_diff_vals_flight_two(self, val):
        se = test_instantiate_schema_engine()

        assert isinstance(se.rounded_len(se.longchar_lengths, val), int)

        n = se.rounded_len(se.longchar_lengths, val)
        assert n == abs(n)

        assert se.rounded_len(se.longchar_lengths, val) in se.longchar_lengths

    @given(val=st.integers(min_value=256, max_value=5000))
    def test_rounded_len_strict(self, val):
        se = test_instantiate_schema_engine()

        with pytest.raises(AssertionError):
            assert se.rounded_len(se.text_lengths, val)

        assert se.rounded_len(se.text_lengths, val, strict=False) >= abs(val)
        assert se.rounded_len(se.text_lengths, val,
                              strict=False) not in se.text_lengths

    def test_rounded_len_spec_vals(self):
        se = test_instantiate_schema_engine()

        test_lengths = [5, 10, 15, 20]

        assert se.rounded_len(test_lengths, 4) == 5
        assert se.rounded_len(test_lengths, 12) != 20
        assert se.rounded_len(test_lengths, 7) != 5

    @given(encoding=st.sampled_from(('utf-8',)),
           read_file=st.sampled_from((INV_TEST_REG, INV_TEST_NH, INV_TEST_PRO,
                                      INV_TEST_PIPE, INV_TEST_WH,
                                      INV_TEST_TAB)))
    def test_build_csv_reader(self, read_file, test_file, encoding):
        dd = test_instantiate_dialect_detector()
        se = test_instantiate_schema_engine()
        working_file = test_file

        with open(read_file, "rt", encoding=encoding) as r, open(
                working_file, "wt", errors="replace") as w:
            for line in r.readlines():
                w.write(line)

        with Path(working_file) as p:
            assert p.exists()
            assert p.stat().st_size > 0

        working_dialect = dd.sniff_for_dialect(working_file)
        working_delimiter = working_dialect.delimiter
        working_quotechar = working_dialect.quotechar
        gen_reader = se.build_csv_reader(working_file,
                                         file_delimiter=working_delimiter,
                                         file_quotechar=working_quotechar)
        assert isinstance(gen_reader, GeneratorType)
        assert isinstance(next(gen_reader), list)

    def test_proc_rows_to_dict(self):
        dd = test_instantiate_dialect_detector()

        headers = dd.sniff_for_headers(INV_TEST_REG)
        csv_reader = SchemaEngine.build_csv_reader(INV_TEST_REG,
                                                   file_delimiter=',',
                                                   file_quotechar='"')

        processed = SchemaEngine()._proc_rows_to_dict(headers, csv_reader)

        assert isinstance(processed, defaultdict)
        assert isinstance(processed["FileType"], list)
        assert isinstance(processed["FileType"][0], tuple)

        for _, det_type in processed["Cost"]:
            assert det_type is float

        for _, det_type in processed["Year"]:
            assert det_type is int

        for _, det_type in processed["Description"]:
            assert det_type is str or not det_type

        for _, det_type in processed["SoldDate"]:
            assert not det_type

    def test_proc_str_to_subtype(self):
        se = test_instantiate_schema_engine()

        assert se._proc_str_to_subtype(0).startswith("Text Width")
        assert se._proc_str_to_subtype(10).startswith("Text Width")
        assert not se._proc_str_to_subtype(265).startswith("Text Width")

        assert se._proc_str_to_subtype(265).startswith("LongChar Width")
        assert se._proc_str_to_subtype(5000).startswith("LongChar Width")
        assert not se._proc_str_to_subtype(0).startswith("LongChar Width")

    def test_proc_dict_to_schema_vals(self):
        dd = test_instantiate_dialect_detector()
        se = test_instantiate_schema_engine()

        headers = dd.sniff_for_headers(INV_TEST_REG)
        csv_reader = SchemaEngine.build_csv_reader(INV_TEST_REG,
                                                   file_delimiter=',',
                                                   file_quotechar='"')

        processed = se._proc_rows_to_dict(headers, csv_reader)

        schema_values = se._proc_dict_to_schema_vals(processed, processed)

        assert isinstance(schema_values, list)
        for pair in schema_values:
            assert isinstance(pair, tuple)
            for part in pair:
                assert isinstance(part, str)

        assert ('Cost', 'Double') in schema_values
        assert ('Description', 'LongChar Width 5000') in schema_values
        assert ('Year', 'Double') not in schema_values

    def test_build_schema_str(self):
        se = test_instantiate_schema_engine()
        schema_str = se.build_schema_str(INV_TEST_REG)

        assert isinstance(schema_str, str)

        for ln in schema_str.split("\n"):
            assert ln.startswith("[") or ln.startswith(
                "Format=") or ln.startswith("Col")
        assert schema_str.startswith("[inv_test.csv]")
        assert "Format=CSVDelimited" in schema_str
        assert schema_str.endswith("Col68=ImageModifiedDate Text Width 50")


'''
class TestIntegrityCheck:

    @given(infile_path=st.sampled_from((INV_TEST_REG, INV_TEST_NH, INV_TEST_PRO,
                                        INV_TEST_PIPE, INV_TEST_WH, INV_TEST_TAB,
                                        INV_TEST_BAD)))
    def test_diff_files(self, infile_path):

        returned = integrity_check(infile_path)
        assert returned
        assert isinstance(returned, str)

    def test_ret_str_equality(self):
        infile_path = INV_TEST_BAD
        prev_ret = INTEG_RET

        with open(prev_ret, "rt") as test_str:
            assert integrity_check(infile_path) == test_str.read()
'''


def main():
    pass


if __name__ == "__main__":
    pytest.main()
