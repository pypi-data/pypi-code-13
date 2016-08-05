from setuptools import setup


setup(name="sdlib_v1.1",
  version="1.1",
  description="Easily integrate developer driver with BuildingOS platform.",
  author="Malcolm I. Monroe", 
  author_email="malcolmian.monroe@gmail.com",
  url="https://github.com/mmonroe86/sdlib.git",
  py_modules=["dvr_mache", "dvr_logger", "dvr_requester"],
  install_requires=[
    "pymongo",  
    "python-logstash",
    "requests",
    "celery",
    "flower",
    "uwsgi",  
  ],
  zip_safe=False
)
