"""this is my very first python program, it can list all items no matter it has nested lists or not"""
def listmass(tdd):
	for items in tdd:
		if isinstance (items,list):
			listmass(items)
		else:
			print (items)
