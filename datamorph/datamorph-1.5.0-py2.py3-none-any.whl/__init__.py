# coding=utf-8

import re
import os
import copy

import datamorph.filters


def prepare(schema, data):
    """Prepare data.

    :param schema: result JSON schema.
    :type schema: dict.
    :param data: JSON data.
    :type data: any.
    :results: prepared schema, data and flag.
    :rtype: tuple.
    """
    prepared = False

    if len(schema) <= 1:
        return schema, data, prepared

    if all(isinstance(value, str) for value in schema.values()):
        common_path = os.path.commonprefix(schema.values())

        if '.' in common_path:
            common_path = common_path.rsplit('.', 1)[0]

            data = extract(data, common_path)

            for key, path in schema.items():
                schema[key] = path[len(common_path) + 1:]

            prepared = True

    return schema, data, prepared


def morph(schema, data):
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

    schema, data, prepared = prepare(schema, data)

    if prepared and isinstance(data, list):
        return morph_many(schema, data)

    for key, paths in schema.items():
        if isinstance(paths, dict):
            result[key] = morph(paths, data)
            continue

        elif isinstance(paths, str):
            paths = [paths]

        for path in paths:
            if '{' in path:
                value = fill(path, data)
            else:
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
        results.append(morph(copy.copy(schema), item))

    return results


def extract(data, path, default=None):
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
                    return default

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
        except (TypeError, KeyError):
            return default

        paths = paths[1:]

    return data


def fill(template, data):
    """Fill string template like a str.format() using nested access to data.

    :param template: template for filling.
    :type template: str.
    :param data: data for filling.
    :type data: list or dict.
    """

    def get_field(template):
        start = None
        in_string = False

        for i, symbol in enumerate(template):
            if symbol == '\'' and template[i-1] != '\\':
                in_string = not in_string
            elif symbol == '{' and not in_string:
                start = i
            elif symbol == '}' and start is not None and not in_string:
                return template[start + 1: i]

    while True:
        field = get_field(template)

        if not field:
            break

        path, *filters = field.split('|', 1)

        if filters:
            filters = datamorph.filters.parse_filters(filters[0])

        value = str(extract(data, path, ''))

        for name, args in filters:
            value = getattr(datamorph.filters, name)(value, *args)

        template = template.replace('{{{}}}'.format(field), value)

    return template
