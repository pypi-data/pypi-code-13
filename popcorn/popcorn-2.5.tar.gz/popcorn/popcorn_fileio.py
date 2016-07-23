
# Popcorn 2.5
# https://github.com/InitializeSahib/Popcorn


class PopFileIO:

    def __init__(self):
        self._file_contents = ""
        self._file_name = ""
        self._string_to_write = ""

    def __init__(self, file_name):
        self._file_name = file_name
        self._string_to_write = ""
        self._file_contents = ""
    @property
    def file_contents(self):
        return self._file_contents

    @file_contents.setter
    def file_contents(self, file_contents):
        self._file_contents = file_contents

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        self._file_name = file_name

    @property
    def string_to_write(self):
        return self._string_to_write

    @string_to_write.setter
    def string_to_write(self, string_to_write):
        self._string_to_write = string_to_write

    def write_string_to_file(self):
        with open(self.file_name, "wt") as output_stream:
            output_stream.write(self.string_to_write)
            output_stream.close()

    def read_file(self):
        with open(self.file_name, "rt") as input_stream:
            self.file_contents = input_stream.read()
            input_stream.close()
