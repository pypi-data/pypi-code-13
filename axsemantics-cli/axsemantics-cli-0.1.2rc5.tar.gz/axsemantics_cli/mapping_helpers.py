# mapping helper functions


def normalize_key(key):
    pattern = re.compile('[^A-Za-z0-9_]')
    key = key.strip()
    key = pattern.sub('', key)
    return key


def splitdata(field, key, row_separator, value_separator):
    """
    splits a list of key-value-pairs

    example: if your data looks like
    name=max;age=14;size=160

    then you can use splitdata with params={'row_separator': ';', 'value_separator': '='}
    which will turn this data into three keys name, age and size
    """
    data = {}
    try:
        pairs = field.split(row_separator)
    except AttributeError:
        return data

    for pair in pairs:
        key, value = pair.split(value_separator)
        key = normalize_key(key)
        data[key] = value.strip()
    return data


def splitlist(field, key, separator):
    """
    splits a list of values into an actual list

    example: given the data
    S,M,L,XL,XXL

    you can use splitlist with params={'separator': ','}
    which will result in the data ["S", "M", "L", "XL", "XXL"]
    """
    data = [element.strip() for element in field.split(separator)]
    return {key: data}


def int_uid(field, key):
    """
    sets the key to be used as uid field, which also makes sure that uid must be a number

    we require a field explicityl named "uid" which must contain unique numbers for each data entry

    example:
    your data objects all have the key "ID", which holds a number for each object

    using int_uid as a mapping function without params will rename the field to uid and make sure it only contains integers

    note: calling a mapping function without params looks generally like this:
    {
      ...
      'ID': [int_uid, {}]
      ...
    }
    """
    try:
        return {'uid': str(int(field))}
    except TypeError:
        if field is None:
            raise KeyError('uid field must not be None') from None
        raise
