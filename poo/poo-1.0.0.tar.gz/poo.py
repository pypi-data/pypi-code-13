'''this is a module used to iterate data in nested lists'''


grocery=['rice','wheat',['milk','water',['juice','meat']]]
def print_lol(the_list):
         for each in the_list:
          if isinstance(each,list):
           print_lol(each)
          else:
           print(each)

print_lol(grocery)
