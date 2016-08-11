from json import dumps as json_dumps

types_golang = {
    "boolean": "bool",
    "integer": "int",
    "number": "float64",
    "object": "map[string]interface{}"
}


def _value_type(type_name, enum):
    if type_name == "interface{}" and enum:
        type_name = "string"

    if type(type_name) is list:
        if len(type_name) == 2 and "null" in type_name:
            type_name = filter(lambda value: value != "null", type_name)[0]
        else:
            type_name = "interface{}"

    if type_name in types_golang:
        type_name = types_golang[type_name]
    return type_name


def golang_type_filter(value):
    result = type_name = _value_type(value.get("type", "interface{}"), "enum" in value)

    if type_name == "array":
        array_type = "interface{}"
        items = value.get("items", None)
        if items:
            array_type = _value_type(items.get("type", "interface{}"), "enum" in value)

        result = "[]" + array_type

    return result

type_filter = lambda value, expected: type(value) == expected
intersection_any_filter = lambda arr1, arr2: len(set(arr1).intersection(arr2)) > 0
intersection_value_filter = lambda arr1, arr2: list(set(arr1).intersection(arr2))[0]
json_dumps_filter = lambda value: json_dumps(value, indent=2, separators=(",", ": "))
upper_camel_case_filter = lambda value: "".join([word.capitalize() for word in value.split("_")])

