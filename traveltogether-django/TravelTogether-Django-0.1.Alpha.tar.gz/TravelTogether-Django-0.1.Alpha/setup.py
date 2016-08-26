from setuptools import setup, find_packages

with open('README.md') as description:
    README = description.read()

with open('requirements.txt') as requirements:
    requirements = requirements.read()

requirements_list = requirements.split('\n')


setup(
    name="TravelTogether-Django",
    version="0.1 Alpha",
    packages=find_packages(),
    author="Boris Altanov",
    author_email="borisaltanov@gmail.com",
    description="Simple carpool webapp using Django",
    long_description=README,
    license="GNU GPL v2",
    url="https://github.com/borisaltanov/TravelTogether",
    install_requires=requirements_list,

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
    ]
)
