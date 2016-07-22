import QuantLib as ql
from .converters import QuantLibConverter as qlf


class TemplateBase(object):
    _inst_map = {}

    def __init__(self, prefix, convention_keys):
        self._instance_name = prefix
        self._iid = NameBase.toid(prefix)
        self._inst_map[self._instance_name] = self.__class__
        self._convention_keys = convention_keys
        self._creator = None

    @property
    def instance_name(self):
        return self._instance_name

    @property
    def iid(self):
        """
        Get instance id
        :return: Instance id
        """
        return self._iid

    @classmethod
    def lookup_template(cls, field_id):
        c_name = field_id.split(".")[0]
        c = cls._inst_map[c_name]
        return getattr(c, "lookup")(field_id)

    def get_creator(self):
        return self._creator

    def _set_creator(self, creator):
        if self._creator is None:
            self._creator = creator
        else:
            raise ValueError("Creator %s attempted to overwrite creator %s in template %s" %(
                creator.__name__, self._creator.__name__, self.id
            ))

    def get_convention_keys(self):
        return self._convention_keys


class NameBase(object):
    """
    All named entities should inherit this class. Every class that inherits this
    class must have a class variable "_id_map = {}" defined. This helps to give
    each class a reverse lookup of name to class mapping.
    """

    def __init__(self, name, name_id=None, prefix="", desc=None):
        prefix += "." if len(prefix) else ""
        name_id = name_id or self.toid(name)
        self._id = prefix+name_id
        self._name = name
        if self._id_map.has_key(self._id):
            raise ValueError("Duplicate id "+self._id)
        else:
            self._id_map[self._id] = self
        self._desc = desc or name

    def __str__(self):
        return self._name

    def __repr__(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @staticmethod
    def toid(name):
        return ''.join(x for x in name.title() if not x.isspace())

    @classmethod
    def lookup(cls, field_id):
        return cls._id_map[field_id]

    @property
    def description(self):
        return self._desc


class TypeName(NameBase):
    _id_map = {}

    def __init__(self, name, type, converter):
        super(TypeName, self).__init__(name)
        self._type = type
        self._converter = converter
        self._outer = self
        self._inner = None

    @property
    def type(self):
        return self._type

    def convert(self, value):
        value = self._converter(value)
        return value


class TypeNameModifier(TypeName):

    def __call__(self, type_name, converter):
        assert(isinstance(type_name, TypeName) == True)
        new_type = TypeName("%s(%s)"%(self.name, type_name.name), self.type, converter)
        new_type._outer = self
        new_type._inner = type_name
        return new_type


def to_list(element_converter):
    def to_list_func(value):

        value = [element_converter(v) for v in value]
        return value
    return to_list_func

_LIST = TypeNameModifier("List Of", list, list)

class DataType(object):
    TEMPLATE = TypeName("Template", TemplateBase, qlf.to_template)
    INT = TypeName("Integer", int, int)
    FLOAT = TypeName("Float", float, float)
    STRING = TypeName("String", str, str)
    BOOL = TypeName("Boolean", bool, bool)
    DICT = TypeName("Dict", dict, dict)
    LIST = TypeName("List", list, list)

    OBJECT = TypeName("Object", object, lambda x: x)
    COMPOUNDING = TypeName("Compounding", int, qlf.to_compounding )
    DATE = TypeName("Date", ql.Date, qlf.to_date)
    FREQUENCY = TypeName("Frequency", int, qlf.to_frequency)  # this is enum for frequency
    DAYCOUNT = TypeName("Day Count", ql.DayCounter, qlf.to_daycount)
    DAY_CONVENTION = TypeName("Day Convention", int, qlf.to_day_convention)  # this is enum for day convention
    CALENDAR = TypeName("Calendar", ql.Calendar, qlf.to_calendar)
    PERIOD = TypeName("Period", ql.Period, qlf.to_period)
    DATE_GENERATION = TypeName("Date Generation", int, qlf.to_date_generation)
    TERM_STRUCTURE_YIELD = TypeName("Term Structure Yield", ql.YieldTermStructure, lambda x: x)
    PRICING_ENGINE = TypeName("Pricing Engine", ql.PricingEngine, lambda x: x)

    LIST_INT = _LIST(INT, to_list(int))
    LIST_DATE = _LIST(DATE, to_list(qlf.to_date))
    LIST_FLOAT = _LIST(FLOAT, to_list(float))


class CategoryName(NameBase):
    _id_map = {}

    def __init__(self, name, desc=None):
        super(CategoryName, self).__init__(name, desc=desc)


class Category(object):

    # termstructure categorization
    TERM_STRUCTURE = CategoryName("Term Structure")  # Term structure categorization
    CREDIT = CategoryName("Credit")
    INFLATION = CategoryName("Inflation")
    VOLATILITY = CategoryName("Volatility")
    YIELD = CategoryName("Yield")


    # Asset names
    FIXED_INCOME = CategoryName("FI", "Fixed Income")
    EQUITY = CategoryName("EQ", "Equity")

    # Security types
    GOVERNMENT = CategoryName("Govt", "Government")
    CORPORATE = CategoryName("Corp", "Corporate")

    # Security subtype
    BOND = CategoryName("Bond")
    ZCB = CategoryName("ZCB", "Zero Coupon Bond")

    MAIN = CategoryName("Main", "A generic category name" )

    # Other category headings
    TIME = CategoryName("Time", "Time module")
    ENGINE = CategoryName("Engine", "Engine module")
    INSTRUMENT = CategoryName("Instrument", "Instrument module")

