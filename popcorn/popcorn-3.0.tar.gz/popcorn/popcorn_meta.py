
# Popcorn 3.0
# https://github.com/InitializeSahib/Popcorn
from functools import wraps


class FunctionMeta:

    def disable(func):
        @wraps(func)
        def disabled_func_wrapper(*args, **kwargs):
            def disabled_func(*args, **kwargs):
                msg = "The function " + func.__qualname__ + " has been disabled."
                print(msg)
            return disabled_func(*args, **kwargs)
        return disabled_func_wrapper

    def show_message(message=""):
        def showing_function(infunc):
            @wraps(infunc)
            def func_wrapper(*args, **kwargs):
                print(message)
                return infunc(*args, **kwargs)
            return func_wrapper
        return showing_function

    def deprecate(func):
        @wraps(func)
        def deprecated_function_wrapper(*args, **kwargs):
            print("The function ", func.__qualname__, " is deprecated, and may be removed in a future release.")
            return func(*args, **kwargs)
        return deprecated_function_wrapper


class VerboseMetaclass(type):

    def __new__(cls, class_name, class_bases, class_dictionary):
        print("Creating class with name ", class_name)
        print("Bases of class are ", class_bases)
        print("Dictionary of class is ", class_dictionary)
        class_object = super().__new__(cls, class_name, class_bases, class_dictionary)
        return class_object
