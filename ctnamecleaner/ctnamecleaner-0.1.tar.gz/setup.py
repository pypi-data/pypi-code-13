from setuptools import setup

setup(author="Jake Kara",
      author_email="jake@jakekara.com",
      url="http://jakekara.com",
      name="ctnamecleaner",
      description="Replace village and commonly-misspelled Connecticut town names with real town names.",
      long_description=open("README.txt").read(),
      version="0.1",
      requires=["pandas","argparse"],
      packages=["ctlookup"],
      scripts=["ctclean"],
      license="GPL")
