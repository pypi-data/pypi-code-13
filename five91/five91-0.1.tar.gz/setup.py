from setuptools import setup

setup(name='five91',
      version='0.1',
      description='Simple 591.com.tw wrapper',
      url='http://github.com/tzengyuxio/python-five91',
      author='Tzeng Yuxio',
      author_email='tzengyuxio@gmail.com',
      license='MIT',
      packages=['five91'],
      install_requires=[
          'beautifulsoup4',
      ],
      zip_safe=False)
