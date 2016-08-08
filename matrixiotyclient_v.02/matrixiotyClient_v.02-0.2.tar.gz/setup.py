from setuptools import setup

setup(name="matrixiotyClient_v.02",
  version="0.2",
  description="WIP Client package",
  author="matrixioty",
  author_email="matrixioty@gmail.com",
  url="https://gitlab.com/chiton-corp/matrix-infrastructure",
  py_modules=["matrix_interface"],
  install_requires=[
    "requests"
  ],
  zip_safe=False
)
