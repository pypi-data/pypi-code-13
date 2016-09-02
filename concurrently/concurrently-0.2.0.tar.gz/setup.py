from setuptools import setup, find_packages

setup(
    name='concurrently',
    version='0.2.0',
    packages=find_packages(exclude=['tests', 'examples']),
    url='https://github.com/sirkonst/concurrently',
    license='MIT',
    author='Konstantin Enchant',
    author_email='sirkonst@gmail.com',
    description=
        'Library helps easy write concurrent executed code blocks.'
        ' Supports asyncio coroutines, threads and processes',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: Russian',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
    ],
)
