from setuptools import setup

setup(
    name='testvsfs',  # name on PyPI
    packages=['testVSFS'],    # package name
    version='0.1.1',
    description='VSFS test example',
    author='Mladenl',
    author_email='mladen.lazarevic@sbgenomics.com',
    url='https://github.com/sbg/vsfs-bix-test', # git repo
    # py_modules=['testVSFS/generate_bash'], # modules are names of specific scripts
    install_requires=[
        'openpyxl', 'docopt==0.6.1', 'rabix'
    ],
    entry_points={
            'console_scripts':
            ['testvsfs = testVSFS.generate_bash:main']
    },
    package_data={
        'testVSFS': ['input_apps_database.xlsx', 'bix-demo-apps.tar'],
    },
    include_package_data=True,
)
