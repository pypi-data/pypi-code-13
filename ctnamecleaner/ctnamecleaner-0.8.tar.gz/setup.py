from setuptools import setup

setup(author="Jake Kara",
      author_email="jake@jakekara.com",
      url="https://github.com/jakekara/ctnamecleaner-py",
      name="ctnamecleaner",
      description="Replace village and commonly-misspelled Connecticut town names with real town names.",
      long_description=open("README.txt").read(),
      version="0.8",
      install_requires=["pandas","argparse"],
      packages=["ctlookup"],
      package_data={"ctlookup":["data/ctnamecleaner.csv"]},
      scripts=["ctclean"],
      license="GPL")
