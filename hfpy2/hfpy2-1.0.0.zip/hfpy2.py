def print_lol(the_list):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)

'''This is the standard comments in Python'''

new= [12,[33,44],65,[37,68],90]

print_lol(new)