from file_readers.data_collector import BaseDataCollector
from openpyxl.cell import column_index_from_string


class SimpleExcelDataCollector(BaseDataCollector):

    def __init__(self, use_header, debug=False):
        self.use_header = use_header
        self.debug = debug
        self.data = []
        self.headers = []

    def collect_data(self, source):
        """Collects all data from a sheet

        Args:
            source: A list or tuple of Cell objects
        """
        if self.use_header:
            self.__collect_with_header(source)
        else:
            self.__collect_as_list(source)

    def __collect_with_header(self, source):
        row = {}
        for cell_object in source:
            if len(cell_object.coordinate) == 2 and "1" in cell_object.coordinate:
                self.headers.append(cell_object.value)
                continue

            index = column_index_from_string(cell_object.coordinate[0]) - 1
            header = self.headers[index]
            row[header] = cell_object.value
        if self.debug:
            print(row)
        if row:
            self.data.append(row)

    def __collect_as_list(self, source):
        row = []
        for cell_object in source:
            row.append(cell_object.value)
        if self.debug:
            print(row)
        if row:
            self.data.append(row)
