from setuptools import setup

setup(
    name="imshow",
    version="0.0.3",
    author="Jonathan Terhorst",
    author_email="terhorst@gmail.com",
    description="Command line tool to visualize numeric arrays.",
    license="GPL",
    keywords="imshow matlab visualize plot array",
    url='https://github.com/terhorst/imshow',
    packages=['imshow'],
    install_requires=[
        'matplotlib', 'numpy'
    ],
    entry_points={
        'console_scripts': [
            'imshow = imshow.imshow:main'
        ]
    })
