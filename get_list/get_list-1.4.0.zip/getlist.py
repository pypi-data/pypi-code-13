def print_list(the_list,indent=False,level = 0,fn=sys.stdout) :
    for each_item in the_list :
        if isinstance(each_item,list) :
            print_list(each_item,indent,level + 1,fn)            
        else :
            if indent :
                for num in range(level):
                    print('\t',end='',file= fn)          
            print(each_item,file = fn)



