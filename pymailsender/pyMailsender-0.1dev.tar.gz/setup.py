from distutils.core import setup

setup(
    name='pyMailsender',
    version='0.1dev',
    description='Package that facilitates mailing from one gmail account to another',
    author='Arima Vu Ram',
    author_email='arima.ram92@gmail.com',
    packages=['pyMailsender',],
    license='MIT',
    zip_safe=False,
    long_description=open('README.txt').read)