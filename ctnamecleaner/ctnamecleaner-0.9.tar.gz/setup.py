import sys
from setuptools import setup

try:
    setup(author="Jake Kara",
          author_email="jake@jakekara.com",
          url="https://github.com/jakekara/ctnamecleaner-py",
          download_url="https://pypi.python.org/pypi/ctnamecleaner/",
          name="ctnamecleaner",
          description="Replace village and commonly-misspelled Connecticut town names with real town names.",
          long_description=open("README.txt").read(),
          version="0.9",
          install_requires=["pandas","argparse"],
          packages=["ctlookup"],
          package_data={"ctlookup":["data/ctnamecleaner.csv"]},
          scripts=["ctclean"],
          license="GPL")
except:
    print ":( Error occurred: " + str(e)
    
