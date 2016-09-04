from setuptools import setup, find_packages

setup(
    name="RecycleBin",
    version="0.1",
    description="A program that will open the Recycle Bin for you only using Alt + R",
    author="Nithish Narasimman",
    author_email="nithishbn@yahoo.com",
    scripts=['theoriginalrecyclebin.py'],
    packages=find_packages(),
    install_requires=['pyhooked'],
)
