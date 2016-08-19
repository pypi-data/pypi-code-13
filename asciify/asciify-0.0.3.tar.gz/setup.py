from setuptools import setup, find_packages

setup(
    name="asciify",
    packages=find_packages(),
    version="0.0.3",
    description="Fun little project",
    long_description="",
    url="https://github.com/paolopaolopaolo/ascii_text_generator/",
    license="GNU",
    author="Dean Mercado",
    author_email="dpaolomercado@gmail.com",
    setup_requires=[
        "click==6.6"
    ],
    install_requires=[
        "click==6.6"
    ],
    test_suite="",
    entry_points={
        "console_scripts": [
            "asciify=asciify.asciify:main",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
    ]
)