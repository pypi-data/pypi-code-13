
# Popcorn 2.4.2
# https://github.com/InitializeSahib/Popcorn


class PopFileIO:

    file_contents = ""
    string_to_write = ""
    file_name = ""

    def get_file_contents(self):
        return self.file_contents

    def set_file_name(self, file_name):
        self.file_name = file_name

    def set_string_to_write(self, string_to_write):
        self.string_to_write = string_to_write

    def write_string_to_file(self):
        with open(self.file_name, "wt") as output_stream:
            output_stream.write(self.string_to_write)

    def read_file(self):
        with open(self.file_name, "rt") as input_stream:
            self.file_contents = input_stream.read()
