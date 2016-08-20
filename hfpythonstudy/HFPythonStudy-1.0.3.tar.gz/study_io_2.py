import os

try:
    if os.path.exists("./sketch.txt"):  # 判断文件是否已经存在
        # 使用with xxx as name 这样的代码，可以自动close，和C#里的using类似
        with open("./sketch.txt") as sketch_file, open("./sketchSaid.txt", mode="w") as new_file:
            for each_line in sketch_file:
                if not each_line.find(":") == -1:
                    (role, message) = each_line.split(
                        ":", maxsplit=1)  # maxsplit参数指定分裂几次
                    print(role, "said:", message, end="",
                          file=new_file)  # file参数指定输出的流
                else:
                    pass
        
        # 再次打开文件验证输出
        with open("./sketchSaid.txt") as new_file:
            for each_line in new_file:
                print(each_line, end='')
    else:
        print("No such file!")
except IOError as err:
    print("File error:" + str(err))

print("\r\nOver..")
