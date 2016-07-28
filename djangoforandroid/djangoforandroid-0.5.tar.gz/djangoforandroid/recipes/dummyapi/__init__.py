from pythonforandroid.toolchain import PythonRecipe

class DummyapiRecipe(PythonRecipe):

    version = "tip"
    url = "https://bitbucket.org/yeisoneng/python-dummyapi/get/{version}.tar.gz"
    depends = ["python3crystax"]

recipe = DummyapiRecipe()
