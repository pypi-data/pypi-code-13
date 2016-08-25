from setuptools import setup

setup(author="Jake Kara",
      author_email="jake@jakekara.com",
      url="http://jakekara.com",
      name="fec",
      description="Simple FEC API wrapper",
      long_description=open("README.txt").read(),
      version="0.0",
      requires=["requests"],
      LICENSE="GPL",
      packages=["fec"])
