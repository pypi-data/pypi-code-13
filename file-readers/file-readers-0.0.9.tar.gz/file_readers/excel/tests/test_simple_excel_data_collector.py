from unittest import TestCase
import os
from file_readers.excel.excel_reader import ExcelReader
from file_readers.excel.simple_excel_data_collector import SimpleExcelDataCollector
from file_readers.excel.tests.simple_cell import SimpleCell
from openpyxl.cell import Cell


base_path = os.path.dirname(__file__)


class TestSimpleExcelDataCollector(TestCase):

    def test_collect_data_with_header(self):
        data_source = []
        row = (SimpleCell("A1", "Name"),
               SimpleCell("B1", "Age"),
               SimpleCell("C1", "Title"))
        data_source.append(row)

        row = (SimpleCell("A2", "John"),
               SimpleCell("B2", 24),
               SimpleCell("C2", "Developer"))
        data_source.append(row)

        collector = SimpleExcelDataCollector(use_header=True)
        for row in data_source:
            collector.collect_data(row)

        result_row = collector.data[0]
        self.assertEqual(result_row['Name'], 'John')
        self.assertEqual(result_row['Age'], 24)
        self.assertEqual(result_row['Title'], "Developer")

    def test_collect_data_without_header(self):
        data_source = []
        row = (SimpleCell("A1", "Name"),
               SimpleCell("B1", "Age"),
               SimpleCell("C1", "Title"))
        data_source.append(row)

        row = (SimpleCell("A2", "John"),
               SimpleCell("B2", 24),
               SimpleCell("C2", "Developer"))
        data_source.append(row)

        collector = SimpleExcelDataCollector(use_header=False)
        for row in data_source:
            collector.collect_data(row)
        result_row = collector.data[0]
        self.assertEqual("Name", result_row[0])
        self.assertEqual("Age", result_row[1])
        self.assertEqual("Title", result_row[2])

        result_row = collector.data[1]
        self.assertEqual("John", result_row[0])
        self.assertEqual(24, result_row[1])
        self.assertEqual("Developer", result_row[2])

    def test_with_reader_using_headers(self):
        test_file = base_path + "/data/test.xlsx"
        collector = SimpleExcelDataCollector(use_header=True)
        reader = ExcelReader(data_collector=collector)
        reader.set_sheet_to_read("Personnel")
        reader.read_file(test_file)
        result_row = collector.data[0]
        self.assertEqual(result_row['Name'], 'John')
        self.assertEqual(result_row['Age'], 24)
        self.assertEqual(result_row['Title'], "Developer")

    def test_with_reader_not_using_headers(self):
        test_file = base_path + "/data/test.xlsx"
        collector = SimpleExcelDataCollector(use_header=False)
        reader = ExcelReader(data_collector=collector)
        reader.set_sheet_to_read("Personnel")
        reader.read_file(test_file)
        result_row = collector.data[0]
        self.assertEqual("Name", result_row[0])
        self.assertEqual("Age", result_row[1])
        self.assertEqual("Title", result_row[2])

        result_row = collector.data[1]
        self.assertEqual("John", result_row[0])
        self.assertEqual(24, result_row[1])
        self.assertEqual("Developer", result_row[2])
