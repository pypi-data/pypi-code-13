#this is a module of nexter.py
def print_lol(the_list):

#this is a fuction
    for each_item in the_list:
		    if isinstance(each_item,list):
   		      print_lol(each_item)
		    else:
			      print(each_item)
 
#movies = ["The Holy Grail",1975,"Terry Jones&Terry Gilliam",91, ["Graham Chapamn",["Michael Palin","John Cleese","Terry Gilliam","Eric Idle","Terry Jones"]]]
  
#print_lol(the_list)                        