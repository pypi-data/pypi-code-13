from distutils.core import setup

setup(
    name='therpy',
    version='0.1dev6',
    packages=['therpy',],
    license='Open Source',
    author='Parth Patel',
    author_email='pbpatel@mit.edu',
    install_requires=['pyfits','tabulate','tqdm'],
)

# Run following commands on terminal
# python setup.py sdist
# python setup.py register (ONLY FIRST TIME)
# python setup.py sdist upload