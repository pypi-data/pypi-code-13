# coding=utf-8

import os


def prepare(schema, data):
    """Prepare data.

    :param schema: result JSON schema.
    :type schema: dict.
    :param data: JSON data.
    :type data: any.
    :results: prepared schema and data.
    :rtype: tuple.
    """
    if all(isinstance(value, str) for value in schema.values()):
        common_path = os.path.commonprefix(schema.values()).rsplit('.', 1)[0]
        data = extract(data, common_path)

        for key, path in schema.items():
            schema[key] = path.lstrip('{}.'.format(common_path))

    return schema, data


def morph(schema, data, to_prepare=True):
    """Morph data.

    :param schema: result JSON schema.
    :type schema: dict.
    :param data: JSON data.
    :type data: dict.
    :param to_prepare: prepare data flag.
    :type to_prepare: bool.
    :results: result data.
    :rtype: dict.
    """
    result = {}

    if to_prepare:
        schema, data = prepare(schema, data)

        if isinstance(data, list):
            return morph_many(schema, data)

    for key, paths in schema.items():
        if isinstance(paths, dict):
            result[key] = morph(paths, data, to_prepare=False)
            continue

        elif isinstance(paths, str):
            paths = [paths]

        for path in paths:
            value = extract(data, path)

            if value:
                result[key] = value
                break

    return result


def morph_many(schema, data):
    """Morph data list.

    :param schema: result JSON schema.
    :type schema: dict.
    :param data: JSON data.
    :type data: list.
    :results: result data.
    :rtype: list.
    """
    results = []

    for item in data:
        results.append(morph(schema, item, to_prepare=False))

    return results


def extract(data, path):
    """Extract value by path.

    :param data: JSON data.
    :type data: dict or list.
    :param path: path for search value.
    :type path: str.
    :result: found value or None.
    :rtype: type.
    """
    paths = path.split('.')

    for key in paths:
        if isinstance(data, list):
            if key.isdigit():
                try:
                    data = data[int(key)]
                    continue
                except IndexError:
                    return None

            results = []

            for item in data:
                result = extract(item, '.'.join(paths))

                if isinstance(result, list):
                    results.extend(result)
                elif result:
                    results.append(result)

            return results

        try:
            data = data[key]
        except KeyError:
            return None

        paths = paths[1:]

    return data
