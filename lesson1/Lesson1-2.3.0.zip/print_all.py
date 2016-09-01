def print_all(x):
    for item in x:
        if isinstance(item, list):
            print_all(item)
        else:
            print(item)

def print_all_2(some_list, level = 3):    #定義函式
    for item in some_list:                #表單中的每個item
        if isinstance(item, list):        #如果該item是list
            print_all_2(item, level+1)    #重新執行一次但是level會+1
        else:                                #不是list
            for tab_stop in range(level):    
                print('\t', end='')          #print幾次Tab
            print(item)

def print_all_3(some_list, indent = False, level = 0):#加一個判斷參數:indent
    for item in some_list:                       
        if isinstance(item, list):               
            print_all_3(item, indent, level+1)    
        else:
            if indent:
                for tab_stop in range(level):    
                    print('\t', end='')          
            print(item)

def print_all_4(some_list, indent = False, level = 0, fh = sys.stdout):#加一個輸出檔案的參數，預設為標準輸出
    for item in some_list:                       
        if isinstance(item, list):               
            print_all_4(item, indent, level+1, fh)    
        else:
            if indent:
                for tab_stop in range(level):    
                    print('\t', end='', file = fh)          
            print(item, file = fh)
