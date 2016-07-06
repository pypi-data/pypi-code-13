from pythonforandroid.toolchain import PythonRecipe

class KickappRecipe(PythonRecipe):

    version = "tip"
    url = "https://bitbucket.org/yeisoneng/python-kickapp/get/{version}.tar.gz"
    depends = [("python2", "python3crystax")]

recipe = KickappRecipe()
