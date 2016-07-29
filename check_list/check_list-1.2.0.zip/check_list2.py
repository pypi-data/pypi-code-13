#This function will display a list with layer structure
#For sample test:  cast=['1', '2', '3', ['3_1', '3_1_1', ['3_2', '3_2_2', '3_2_2_2',["3_3","3_3_3","3_3_3_3","3_3_3_3_3"]]]]
def check_list2(the_list):
	for item in the_list:
		if isinstance(item,list):
			#print("\n")
			for item_1 in item:
				if isinstance(item_1,list):
					#print("\n")
					for item_2 in item_1:
						if isinstance(item_2,list):
							#print("\n")
							for item_3 in item_2:
								if isinstance(item_3,list):
									print("\n\t\t\t",end=item_3)
								else:
									print("\n\t\t\t",item_3,end='')
						else:
							print("\n\t\t",item_2,end='')
				else:
					print("\n\t",item_1,end='')
		else:
			print("\n",item,end='')
