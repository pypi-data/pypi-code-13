from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='knowlify',
    version='0.0.1',
    description='Add context dependent information to a html file',
    long_description=readme,
    author='Lotanna Ezenwa',
    author_email='lota.ezenwa@gmail.com',
    url='https://github.com/LotannaEzenwa/knowlify',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)