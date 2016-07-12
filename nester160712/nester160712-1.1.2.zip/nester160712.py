def nester(the_list, level=0):
        for each_item in the_list:
                if isinstance(each_item, list):
                        nester(each_item, level+2)
                else:
                        for num in range(level):
                                print(' ', end='')
                        print(each_item)
