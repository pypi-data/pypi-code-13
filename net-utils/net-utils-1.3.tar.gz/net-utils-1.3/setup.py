from setuptools import setup, find_packages
setup(name="net-utils", 
	author="arron",
	author_email="fsxchen@gmail.com",
	version="1.3",
    	package_data = {'':['*.*']},
	packages=find_packages(),
    	py_modules=['net-utils'],
)
