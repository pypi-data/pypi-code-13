def print_all(x):
    for item in x:
        if isinstance(item, list):
            print_all(item)
        else:
            print(item)

def print_all_2(some_list, level = 3):    #定義函式
    for item in some_list:            #表單中的每個item
        if isinstance(item, list):    #如果該item是list
            print_all_2(item, level+1)#重新執行一次但是level會+1
        else:                                #不是list
            for tab_stop in range(level):    
                print('\t', end='')          #print幾次Tab
            print(item)
