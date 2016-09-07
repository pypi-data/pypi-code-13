#This is a simple for my Python learning, I'm afraid it's not use for you.
movies = ["The Holy Grail", 1975, "Terry Jones & Terry Gilliam", 91, ["Graham Chapman", ["Michael Palin", "John Cleese", "Terry Gilliam", "Eric Idle", "Terry Jones"]]]

def take_list(x, i=0):
    
    for y in x:
        if isinstance(y, list):
            take_list(y, i+1)
        else:
            for z in range(i):
                print("\t", end="")
            print (y)