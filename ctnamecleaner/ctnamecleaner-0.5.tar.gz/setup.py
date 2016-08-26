from setuptools import setup

setup(author="Jake Kara",
      author_email="jake@jakekara.com",
      url="https://github.com/jakekara/ctnamecleaner-py",
      name="ctnamecleaner",
      description="Replace village and commonly-misspelled Connecticut town names with real town names.",
      long_description=open("README.txt").read(),
      version="0.5",
      install_requires=["pandas","argparse"],
      packages=["ctlookup"],
      scripts=["ctclean"],
      license="GPL")
