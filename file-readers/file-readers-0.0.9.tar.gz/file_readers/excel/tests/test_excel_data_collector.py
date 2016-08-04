from unittest import TestCase
from file_readers.excel.excel_data_collector import ExcelDataCollector
from file_readers.excel.tests.simple_cell import SimpleCell
from openpyxl.cell import Cell


class TestExcelDataCollector(TestCase):

    def test_collect_data(self):
        data_source = []
        row = (SimpleCell("A1", "Name"),
               SimpleCell("B1", "Age"),
               SimpleCell("C1", "Title"))
        data_source.append(row)

        row = (SimpleCell("A2", "John"),
               SimpleCell("B2", 24),
               SimpleCell("C2", "Developer"))
        data_source.append(row)

        collector = ExcelDataCollector()
        for row in data_source:
            collector.collect_data(row)

        result_row = collector.data[0]
        self.assertEqual(result_row['Name'], 'John')
        self.assertEqual(result_row['Age'], 24)
        self.assertEqual(result_row['Title'], "Developer")
