import time
def print_name(func):
    print func.__name__
    print time.strftime('now:%c')
