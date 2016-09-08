from setuptools import setup

setup(name='odprep',
      version='0.1.1',
      description='Orders catalog ids and updates delivery status every 10min. Once delivered, processes cat ids and dumps in disaster-open-data bucket',
      url='https://github.com/lizasapphire/odprep',
      author='lizasapphire',
      author_email='lizasapphire@gmail.com',
      license='',
      packages=['odprep'],
      install_requires=[
           'gbdxtools', 'openpyxl', 'requests'

      ],
      zip_safe=False)