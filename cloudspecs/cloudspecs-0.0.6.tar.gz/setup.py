from setuptools import setup, find_packages
import os


def load_data_files(directory='cloudspecs/data'):
    return [(root, [os.path.join(root, f) for f in files])
            for root, dirs, files in os.walk(directory)]

setup(
    name='cloudspecs',
    version='0.0.6',
    author='Mihir Singh (@citruspi)',
    author_email='hello@mihirsingh.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    package_data={'cloudspecs': 'data/aws/ec2/*'},
    platforms='any',
)
