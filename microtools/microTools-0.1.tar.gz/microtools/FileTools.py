def putContents(name, data):
    f=open(name, "w+")
    f.write(data)
    f.close()


def getContents(name):
    f = open(name, "r")
    try:
        return f.read()
    finally:
        f.close()

