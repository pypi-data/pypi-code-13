from setuptools import setup

setup(
    name = "searchie-tools-find_buildout_root",
    description = "Simple utility to search buildout root directory",
    version = "0.0.2",
    maintainer = "Eugene Krokhalev",
    maintainer_email = "rutsh@mlworks.com",
    py_modules = ["find_buildout_root"],
    entry_points = {
        "console_scripts": [
            "find_buildout_root = find_buildout_root:main"
        ]
    },
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities"
    ]
)
