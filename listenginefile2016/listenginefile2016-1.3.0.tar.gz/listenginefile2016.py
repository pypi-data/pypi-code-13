#comment1
#comment2
def list_engine(the_list,indent=False,level=0):
        #comment3
        #comment4
        for each_item in the_list:
                if isinstance(each_item,list):
                        list_engine(each_item,indent,level+1)
                else:
                        if indent:
                                for tab_stop in range(level):
                                        print("\t",end='')
                        print(each_item)
