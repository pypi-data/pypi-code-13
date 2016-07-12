def nester(the_list, level=0, indent=True):
        for each_item in the_list:
                if isinstance(each_item, list):
                        nester(each_item, level+2)
                else:
                        if indent:
                                for num in range(level):
                                        print(' ', end='')
                                print(each_item)
