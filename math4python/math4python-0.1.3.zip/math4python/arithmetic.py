from .string_utility import print_string


def add(x, y):
    return x + y


def multiply(x, y):
    return x * y


def divide(x, y):
    if y == 0:
        print_string("Fuck!! You can't divide a number by 0!")
    else:
        return x / y


def subtract(x, y):
    return x - y
