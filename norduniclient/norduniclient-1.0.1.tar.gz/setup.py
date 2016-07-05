from setuptools import setup, find_packages

version = '1.0.1'

requires = [
    'neo4j-driver>=1.0.0,<2.0.0',
]

testing_requires = [
    'nose',
    'coverage',
    'nosexcover',
]

setup(
    name='norduniclient',
    version=version,
    url='https://github.com/NORDUnet/python-norduniclient',
    license='',
    author='Johan Lundberg',
    author_email='lundberg@nordu.net',
    description='Neo4j (3.0) database client using bolt for NORDUnet network inventory',
    packages=find_packages(),
    zip_safe=True,
    install_requires=requires,
    tests_require=testing_requires,
    test_suite="norduniclient",
    extras_require={
        'testing': testing_requires
    }
)
