from setuptools import setup, find_packages

setup(
    name="nbgen",
    description="Generates a Jupyter Notebook and slides from your data",
    url="https://github.com/ewjoachim/nbgen",
    version="0.1",
    packages=find_packages(exclude=["sample.py"]),
    entry_points={
        'console_scripts': [
            'nbgen = nbgen:main',
        ],
    },
    author="Joachim Jablon",
    author_email="ewjoachim@gmail.com",
    install_requires=['jupyter', 'docopt'],
    keywords=["jupyter", "notebook", "generation", "slides"],
)
