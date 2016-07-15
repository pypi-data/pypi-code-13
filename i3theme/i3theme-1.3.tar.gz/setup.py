
from setuptools import setup, find_packages

import i3theme, os

setup(
    name = "i3theme",
    version = "1.3",
    author="manzerbredes",
    author_email="pip-account@loicguegan.fr",
    description="Simple utility to apply Yaml formated theme to i3wm.",
    license="GPL",
    keywords="i3wm theme",
    long_description=open(os.path.join(os.path.dirname(__file__), "Readme.md")).read(),
    packages = find_packages(),
    install_requires=[
                      "voluptuous"
                      ],
    package_data={'i3theme': ['themes/*']},
    entry_points={
        'console_scripts': [
            'i3theme=i3theme.i3theme:main'
        ]
    },
)
