import os

try:
    if os.path.exists("./sketch.txt"):
        sketch_file = open("./sketch.txt")
        new_file = open("./sketchSaid.txt", mode="w")
        for each_line in sketch_file:
            if not each_line.find(":") == -1:
                (role, message) = each_line.split(":", maxsplit=1)
                print(role, "said:", message, end="", file=new_file)
                print(role, "said:", message, end="")
            else:
                pass
    else:
        print("No such file!")
except IOError as err:
    print("File error:" + str(err))
finally:
    if "sketch_file" in locals():
        sketch_file.close()
    if "new_file" in locals():
        new_file.close()

print("\r\nOver..")
