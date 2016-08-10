"""This is the standard way to
   include a multiple-line comment in
   your code."""

#movies = [ "The Holy Grail", 1975, "Terry Jones & Terry Gilliam", 91, ["Graham Chapman", ["Michael Palin",[1,2,3], "John Cleese", "Terry Gilliam", "Eric Idle", "Terry Jones"]]]

def print_lol(the_list, level):
   """This function takes a positional argument called “the_list",
   which is any Python list (of, possibly, nested lists).
   Each data item in the provided list is (recursively)
   printed to the screen on its own line."""
 
   for each_item in the_list:
       if isinstance(each_item, list):
           
           print_lol(each_item, level+1)
           
       else:
           for each_level in range(level):
              print('  ', end='')
           print(each_item)

#print_lol(movies, 0)


