try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='pocomp',
    packages=["pocomp"],
    entry_points = {"console_scripts": ['pocomp = pocomp.pocomp']},
    install_requires=['polib'],
    requires=['polib'],
    version='0.3',
    keywords="po file compiler",
    license='BSD',
    author='Andrey Bobrovskiy',
    author_email='lasthitknxx@gmail.com',
    description='Simple po files compiler',
    )