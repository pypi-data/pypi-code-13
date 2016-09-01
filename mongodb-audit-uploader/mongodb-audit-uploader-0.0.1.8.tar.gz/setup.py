from setuptools import setup
from pkg_resources import Requirement, resource_filename

setup(name='mongodb-audit-uploader',
      version='0.0.1.8',
      description='Upload MongoDB ',
      url='https://github.com/bookmd/mongodb-audit-uploader',
      author='Ben Waters',
      author_email='ben@book-md.com',
      license='MIT',
      packages=['mongodb_auditor_uploader'],
      install_requires=['elasticsearch'],
      data_files=[('/etc/default/', ['conf/mongodb-audit-uploader'])],
      scripts=['bin/mongodb-auditor-uploader'],
      include_package_data=True,
      zip_safe=True)
