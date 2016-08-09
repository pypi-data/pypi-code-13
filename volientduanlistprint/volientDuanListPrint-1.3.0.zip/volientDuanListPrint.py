def print_isList(this_list,indent=False,level=0,fn=sys.stdout):
	for each_item in this_list:
		if isinstance(each_item,list):
			print_isList(each_item,indent,level+1,fn)
		else:
			if indent:
				print("\t"*level,end='',file=fn)
			print(each_item,file=fn)
			