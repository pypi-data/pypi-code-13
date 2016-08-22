from distutils.core import setup

setup(
    name='libpg_hvm',
    version='0.0.5',
    author='hvm',
    author_email='hvm2hvm@gmail.com',
    packages={'libpg': 'libpg_hvm'},
    scripts=[],
    url='http://blog.voicuhodrea.com',
    license='LICENSE.txt',
    description='simple psycopg2 wrapper',
    long_description=open('README.txt').read(),
    py_modules=[
        "psycopg2",
    ],
)
