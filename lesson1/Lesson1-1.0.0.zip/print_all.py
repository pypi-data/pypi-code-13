def print_all(x):
    for item in x:
        if isinstance(item, list):
            print_all(item)
        else:
            print(item)
