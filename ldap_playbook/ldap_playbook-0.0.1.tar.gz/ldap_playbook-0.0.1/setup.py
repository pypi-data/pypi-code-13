from setuptools import setup, find_packages
PACKAGE = "ldap_playbook"
NAME = "ldap_playbook"
DESCRIPTION = ""
AUTHOR = "jialiang.ni"
AUTHOR_EMAIL = "jialiang.ni"
URL = ""
VERSION = "0.0.1"

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    packages=find_packages(),
    zip_safe=False,
)
