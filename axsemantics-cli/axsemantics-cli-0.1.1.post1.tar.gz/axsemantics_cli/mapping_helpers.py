# mapping helper functions
def splitdata(field, key, row_separator, value_separator):
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
    data = [element.strip() for element in field.split(separator)]
    return {key: data}


def int_uid(field, key):
    try:
        return {'uid': str(int(field))}
    except TypeError:
        if field is None:
            raise KeyError('uid field must not be None') from None
        raise
