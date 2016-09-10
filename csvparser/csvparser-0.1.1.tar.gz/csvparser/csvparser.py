import csv
import decimal


class Parser(object):
    fields_order = None

    @classmethod
    def parse_file(cls, file_path, start_from_line=1, end_at_line=None, csv_reader=csv.reader, **kwargs):
        with open(file_path, 'r') as file:
            reader = csv_reader(file, **kwargs)
            fields = cls.get_all_field_names_declared_by_user()

            for skipped_row in range(1, start_from_line):
                next(reader)

            for line_num, row in enumerate(reader, start=start_from_line):
                if end_at_line is not None and line_num > end_at_line:
                    break

                instance = cls()
                for i, field in enumerate(fields):
                    setattr(instance, field, row[i])
                yield instance

    @classmethod
    def get_all_field_names_declared_by_user(cls):
        return cls.fields_order


class ParserField(object):
    def __init__(self):
        self.name = None
        self.init_done = False

    def __set__(self, instance, value):
        if not self.init_done:
            cls = instance.__class__
            for field, object in cls.__dict__.items():
                if id(object) == id(self):
                    self.name = '_' + field
                    setattr(instance, self.name, value)
                    self.init_done = True
                    break
        else:
            setattr(instance, self.name, value)


class IntegerField(ParserField):
    def __get__(self, instance, cls):
        return int(getattr(instance, self.name))


class DecimalField(ParserField):
    def __get__(self, instance, cls):
        return decimal.Decimal(getattr(instance, self.name))


class CharField(ParserField):
    def __get__(self, instance, cls):
        return getattr(instance, self.name)