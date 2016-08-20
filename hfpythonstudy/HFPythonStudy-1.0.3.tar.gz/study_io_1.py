import os

print("Current work dictory: " + os.getcwd())  # 获取当前的工作路径

try:
    if os.path.exists("./sketch.txt"):  # 判断文件是否已经存在
        sketch_file = open("./sketch.txt")  # 打开文件流
        new_file = open("./sketchSaid.txt", mode="w")  # 打开写入流
        for each_line in sketch_file:
            if not each_line.find(":") == -1:
                (role, message) = each_line.split(
                    ":", maxsplit=1)  # maxsplit参数指定分裂几次
                print(role, "said:", message, end="",
                      file=new_file)  # file参数指定输出的流
                print(role, "said:", message, end="")
            else:
                pass
    else:
        print("No such file!")
except IOError as err:
    print("File error:" + str(err))
finally:
    # “xxx” in locals()，locals()返回当前上下文的所有引用名称的字典，判断是否存在里面，就可以判断是是否已经定义
    if "sketch_file" in locals():
        sketch_file.close()
    if "new_file" in locals():
        new_file.close()

print("\r\nOver..")
