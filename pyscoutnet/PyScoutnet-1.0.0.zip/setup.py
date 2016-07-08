'''
Created on 02.07.2012

@author: Jan Brohl <janbrohl@t-online.de>
@license: Simplified BSD License see license.txt
@copyright: Copyright (c) 2012, Jan Brohl <janbrohl@t-online.de>. All rights reserved.
'''
from setuptools import setup
execfile("src/pyscoutnet/__init__.py")

name = "PyScoutnet"
url = "https://bitbucket.org/janbrohl/" + name.lower()

setup(name=name,
      version=__version__,
      author="Jan Brohl",
      author_email="janbrohl@t-online.de",
      url=url,
      download_url="%s/downloads/%s-%s.zip" % (url, name, __version__),
      package_dir={"": "src"},
      data_files=["license.txt", "src/api_examples.py"],
      license="Simplified BSD see license.txt",
      packages=["pyscoutnet"],
      requires=["requests"],
      description="Access to the Scoutnet.de REST-API"
      )
