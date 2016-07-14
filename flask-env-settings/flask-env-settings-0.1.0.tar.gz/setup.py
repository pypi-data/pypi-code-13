from setuptools import setup

setup(**{
  "name": "flask-env-settings",
  "py_modules": ["flask_env_settings"],
  "url": "https://github.com/dveselov/flask-env-settings",
  "author": "Dmitry Veselov",
  "author_email": "d.a.veselov@yandex.ru",
  "version": "0.1.0",
  "description": "Load application settings from env variables",
  "license": "MIT",
  "classifiers": (
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
  ),
  "install_requires": [
    "Flask>=0.11.1",
  ],
})
