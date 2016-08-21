class Counter():
    def __init__(self, my_number):
        self.my_number = my_number

    def increment(self):
        self.my_number += 1
        return self.my_number

    def number(self):
        return self.my_number


def call_method(method):
    return method()


foo1 = Counter(1)
foo2 = Counter(2)

print(call_method(foo1.increment))
print(call_method(foo1.increment))
print(call_method(foo1.increment))
