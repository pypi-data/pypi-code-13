from qtk.conventions import Convention
from qtk.converters import QuantLibConverter
from qtk.fields import FieldName


class CreatorBaseMeta(type):

    def __new__(mcs, name, bases, dct):
        return super(CreatorBaseMeta, mcs).__new__(mcs, name, bases, dct)

    def __init__(cls, name, bases, dct):
        templates = dct.get("_templates")
        base = dct.get("_base", False)
        if templates is not None:
            if isinstance(templates, list):
                for t in templates:
                    t._set_creator(cls)
            else:
                raise ValueError("_template not of type list")
        elif not base:
            raise AttributeError("Expected _templates class variable definition for creator ", cls)

        req_fields = dct.get("_req_fields")
        if req_fields is not None:
            if isinstance(req_fields, list):
                pass
            else:
                raise ValueError("_req_fields not of type list")
        elif not base:
            raise AttributeError("Expected _req_fields class variable definition for creator ", cls)

        super(CreatorBaseMeta, cls).__init__(name, bases, dct)
        #if name !="CreatorBase":
        #    self.setup_dependency()


class CreatorBase(object):
    """
    Every creator must inherit this class. This class adds properties
    to link every template with a creator in an automated way. In order
    to do this, every class that inherits CreatorBase must define a variable
    "_templates" which is a list of all templates that it can instantiate.
    """
    __metaclass__ = CreatorBaseMeta
    _base = True

    def __init__(self, data, params=None):
        """

        :param data:
        :param params:
        :return:
        """

        self._data = data
        self._data.update(self.defaults())
        self._params = params or {}
        self._template = QuantLibConverter.to_template(self._data["Template"])
        self._convention_keys = self._template.get_convention_keys()
        self._object = None

    def get_convention_key(self):
        return ".".join([self._data[k.id] for k in self._convention_keys] + [self._data["Template"].id])

    def get_global_convention(self):
        return Convention.get(self.get_convention_key())

    @classmethod
    def get_templates(cls):
        return cls._templates

    @classmethod
    def get_req_fields(cls):
        from qtk.fields import Field
        return [Field.TEMPLATE] + cls._req_fields

    @classmethod
    def get_req_field_ids(cls):
        return [f.id for f in cls.get_req_fields()]

    @classmethod
    def _check_fields(cls, data):
        missing_fields = list(set(cls.get_req_field_ids()) - set(data.keys()))
        if len(missing_fields):
            raise AttributeError("Missing fields in " + cls.__name__ + " data: " +
                                 ", ".join([mf for mf in missing_fields]))
        return True

    @classmethod
    def _check_convert_datatypes(cls, data):
        for field_id, val in data.iteritems():
            field = FieldName.lookup(field_id)
            cnvrt_val = field.data_type.convert(val)
            data[field_id] = cnvrt_val
            # if field.data_type == DataType.LIST:
            #    data[field_id] = [cls._check_convert_datatypes(v) for v in cnvrt_val]
        return data

    def check(self):
        self._check_fields(self._data)
        self._check_convert_datatypes(self._data)

    def create(self, asof_date):
        _conventions = self._data.get("Conventions")
        self._conventions = _conventions or self.get_global_convention()
        self._conventions = self._conventions or {}  # default to empty dict if global conventions missing
        self._object = self._create(asof_date)
        self._data["Object"] = self._object
        if self._data.get("ObjectId") is None:
            self._data["ObjectId"] = id(self._object)
        return self._object

    def _create(self, asof_date):
        raise NotImplementedError("Missing method _create for Creator " + self.__class__.__name__)

    def get(self, field, default_value=None):
        field_id = field.id
        if default_value is None:
            conventions = self._conventions.get(field_id)
            return self._data.get(field_id, conventions)
        else:
            return self._data.get(field_id, default_value)

    def __getitem__(self, field):
        return self._data[field.id]

    @property
    def data(self):
        return self._data

    def defaults(self):
        return {}

    #@classmethod
    #def setup_dependency(cls):
    #    raise NotImplementedError("%s has not implemented method setup_dependency" % cls.__name__)

    #@classmethod
    #def output(cls, param_dict=None):
    #    raise NotImplementedError("%s has not implemented method output" % cls.__name__)