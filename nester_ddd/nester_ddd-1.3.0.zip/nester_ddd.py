"""这是nester.py模块，提供了一个print_lol函数"""
def print_lol(the_list,indent=False,level=0):
  """这是一个递归函数，参数为列表，名为the_list"""
  for each_item in the_list:
    if isinstance(each_item,list):
      print_lol(each_item,indent,level+1)
    else:
      if indent:
        for tab_stop in range(level):
          print("\t",end='')
      print(each_item)
