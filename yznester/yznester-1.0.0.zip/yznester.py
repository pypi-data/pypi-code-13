cast = ['Palin','Cleese',['战狼','寒战','天天向上'],'电影',['魔兽','穿越火线','函数']]
def print_lol(the_list,indent=False,level=0):
    for list_item in the_list:
        if isinstance(list_item, list):
            print_lol(list_item,indent,level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t",end="")
            print(list_item)
