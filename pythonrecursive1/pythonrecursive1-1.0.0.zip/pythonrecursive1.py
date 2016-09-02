def recursive(thelist):
	for each_tiem in thelist:
		if isinstance(each_tiem,list):
			recursive(each_tiem)
		else:
			print(each_tiem)
