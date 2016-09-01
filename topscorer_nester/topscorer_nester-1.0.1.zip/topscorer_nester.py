def roof_fn(the_list):
	for each_item in the_list:
		if isinstance(each_item, list):
			roof_fn(each_item)
		else:
			print(each_item)			