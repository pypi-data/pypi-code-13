def print_bansal(the_list):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_bansal(each_item)
        else:
            print(each_item)
            
