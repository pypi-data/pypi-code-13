from setuptools import setup

setup(
    name="ptoken",
    packages=["ptoken", "ptoken.cache"],
    install_requires=["pycrypto", "redis"],
    version="0.1",
    description="Token Helper",
    author="Fallen",
    author_email="tuanlq.it@gmail.com",
    url="https://github.com/tuanlq11/python_token",
    download_url="https://github.com/tuanlq11/python_token/tarball/0.1",
    keywords=["security"],
    classifiers=[]
)
