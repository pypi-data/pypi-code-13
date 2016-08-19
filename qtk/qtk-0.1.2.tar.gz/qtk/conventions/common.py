from .curves import _curves
from .govtbonds import _govt_bonds
from .swaptions import _swaptions


class Convention(object):
    def _merge_dicts(*dict_args):
        """
        Given any number of dicts, shallow copy and merge into a new dict,
        precedence goes to key value pairs in latter dicts.
        :param dict_args:
        :return:
        """
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
        return result

    _dicts = [_govt_bonds, _curves, _swaptions]
    _conventions = _merge_dicts(*_dicts)

    @classmethod
    def get(cls, convention_key):
        return cls._conventions.get(convention_key)