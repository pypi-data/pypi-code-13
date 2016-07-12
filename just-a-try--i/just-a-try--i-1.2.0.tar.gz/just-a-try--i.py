def print_lvl(liste, ebene=0):
    for element in liste:
        if isinstance(element, list):
            print_lvl(element, ebene+1)
        else:
            for tab_stop in range(ebene):
                print(" ", end='')
            print(element)
