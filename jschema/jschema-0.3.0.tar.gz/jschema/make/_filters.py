from json import dumps as json_dumps

types_golang = {
    "boolean": "bool",
    "integer": "int",
    "number": "float64",
    "object": "map[string]interface{}"
}


def golang_type(value):
    type_name = value.get("type")
    if type(type_name) is list:
        type_name = filter(lambda value: value != "null", type_name)[0]

    if type_name == "array":
        array_type = value.get("items").get("type")
        if type(array_type) is list:
            array_type = filter(lambda value: value != "null", array_type)[0]
        if array_type in types_golang:
            array_type = types_golang[array_type]
        result = "[]" + array_type
    else:
        result = type_name
        if type_name in types_golang:
            result = types_golang[type_name]
    return result

type_filter = lambda value, expected: type(value) == expected
intersection_any_filter = lambda arr1, arr2: len(set(arr1).intersection(arr2)) > 0
intersection_value_filter = lambda arr1, arr2: list(set(arr1).intersection(arr2))[0]
json_dumps_filter = lambda value: json_dumps(value, indent=2, separators=(",", ": "))
upper_camel_case_filter = lambda value: "".join([word.capitalize() for word in value.split("_")])
golang_type_filter = golang_type
