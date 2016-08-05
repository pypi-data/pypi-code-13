def print_lol(the_list,indent=False,level=0):
    for each_item in the_list:
        if isinstance(each_item,list):
            if indent:
                print_lol(each_item,indent,level+1)
        else:
            print(each_item)
            
        
