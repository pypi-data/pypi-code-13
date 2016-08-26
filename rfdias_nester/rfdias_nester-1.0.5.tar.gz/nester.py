"""This is the "Nester.py" module ant id provides one function called print_lol()
    which prints lists that may oy may not include nested lists.""" 

def print_lol(the_list,indent=False,level=0,fh=sys.stdout):
    """This function takes one positional argument called "the_list", which
        is any python list ( of - possibly - nested lists). Each data item in the
        provided list is (recursively) printed to the screen on it's own line.
        Um segundo argumento chamado "level" é usado para inserir tabulacoes quando uma lista aninhada e encontrada
        Edit "setup.py" so that it reads."""

    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item,indent,level+1.fh)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end=''. file=fh)
            print(each_item,file=fh)
            
    
