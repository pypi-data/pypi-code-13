from setuptools import setup


setup(name='mongodb-audit-uploader',
      version='0.0.0.1',
      description='Upload MongoDB ',
      url='https://github.com/bookmd/mongodb-audit-uploader',
      author='Ben Waters',
      author_email='ben@book-md.com',
      license='MIT',
      packages=['mongodb_auditor_uploader'],
      install_requires=['elasticsearch'],
      scripts=['bin/mongodb-auditor-uploader'],
      zip_safe=False)