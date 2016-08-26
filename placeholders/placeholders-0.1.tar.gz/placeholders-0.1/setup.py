from setuptools import setup, find_packages

setup(
    name='placeholders',
    version='0.1',
    packages = find_packages(),
    py_modules=['placeholders', 'PDFTools'],
    install_requires=[
        'Click',
        'pyyaml'
    ],
    entry_points='''
        [console_scripts]
        placeholders=placeholders:make_placeholders
    ''',
)
