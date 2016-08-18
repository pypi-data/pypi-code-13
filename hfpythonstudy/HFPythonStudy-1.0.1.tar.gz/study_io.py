try:
    sketch_file = open("./sketch.txt")
    new_file = open("./sketchSaid.txt", mode = "w")
    for each_line in sketch_file:
        if not each_line.find(":") == -1:
            (role, message) = each_line.split(":", maxsplit=1)
            print(role, "said:",message, end="",file=new_file);
            print(role, "said:",message, end="");
        else:
            pass
except IOError:
    pass
finally:
    sketch_file.close()
    new_file.close()

print("\r\nOver..");