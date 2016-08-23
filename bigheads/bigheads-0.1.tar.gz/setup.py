from setuptools import setup

setup(name='bigheads',
      version='0.1',
      description='Scrape topics from GeeksforGeeks and convert to PDF',
      url='https://github.com/arpan14/bighead',
      author='Arpan Mishra',
      author_email='akmish3@gmail.com',
      license='MIT',
      packages=['bigheads'],
      install_requires=[
          'bs4','httplib2','pdfkit'
      ],
      zip_safe=False)