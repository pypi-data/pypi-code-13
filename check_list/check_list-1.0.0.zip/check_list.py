#Python 3.6.0a3 (v3.6.0a3:f3edf13dc339, Jul 11 2016, 21:40:24) [MSC v.1900 64 bit (AMD64)] on win32
#Type "copyright", "credits" or "license()" for more information.
#This function will display a list with 3 layers inside, please add more if&for for additional layers.
def check_list(the_list):
	for item in the_list:
		if isinstance(item,list):
			for item_1 in item:
				if isinstance(item_1,list):
					for item_2 in item_1:
						if isinstance(item_2,list):
							for item_3 in item_2:
								print(item_3)
						else:
							print(item_2)
				else:
					print(item_1)
		else:
			print(item)

			
