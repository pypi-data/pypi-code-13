import os
from print_help import print_lol

try:
    man = []
    other = []
    if os.path.exists("./sketch.txt"):  # 判断文件是否已经存在
        # 使用with xxx as name 这样的代码，可以自动close，和C#里的using类似
        with open("./sketch.txt") as sketch_file, open("./sketchSaid.txt", mode="w") as new_file:
            for each_line in sketch_file:
                if not each_line.find(":") == -1:
                    (role, message) = each_line.split(
                        ":", maxsplit=1)  # maxsplit参数指定分裂几次
                    if role == "Man":
                        man.append(str(message).strip()) # trim的功能
                    else:
                        other.append(str(message).strip())
                else:
                    pass
            print_lol("Man saids.......", out=new_file)
            print_lol(man, out=new_file)
            print_lol("Other saids.......", out=new_file)
            print_lol(other, out=new_file)

        # 再次打开文件验证输出
        with open("./sketchSaid.txt") as new_file:
            for each_line in new_file:
                print(each_line, end='')
    else:
        print("No such file!")
except IOError as err:
    print("File error:" + str(err))

print("\r\nOver..")
