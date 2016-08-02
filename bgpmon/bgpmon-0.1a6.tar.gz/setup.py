from setuptools import setup,find_packages

setup(
    name = "bgpmon",
    version = "0.1a6",
	install_requires = ["suds-jurko"],
    author = "Brett Krueger",
    author_email = "brett@jinsku.com",
    description = ("A simple Python wrapper for the BGPMon SOAP API."),
    license = "MIT",
    keywords = "bgpmon python wrapper",
    url = "https://github.com/brettkrueger/bgpmon/bgpmon/",
	packages=find_packages(exclude=['docs','tests']),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 2.7"
    ],
)
