
def print_lvl(a_list):
    for daten in a_list:
        if isinstance(daten, list):
            print_lvl(daten)
        else:
            print(daten)
