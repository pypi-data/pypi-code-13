from pythonforandroid.toolchain import PythonRecipe

class DjangoforandroidRecipe(PythonRecipe):

    version = "tip"
    url = "https://bitbucket.org/yeisoneng/django-for-android/get/{version}.tar.gz"
    depends = ["python3crystax"]

recipe = DjangoforandroidRecipe()
