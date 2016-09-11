import sys

from setuptools import setup
from setuptools import find_packages

requirements = ['requests']
if sys.version_info < (2, 7):
    requirements.append('argparse')

setup(name='hblock',
      version='0.0.6',
      description='Hostname adblocker in your System Tray',
      long_description="""HBlock is a simple adblocker for Linux application
      and lets you control ads blocking on your system tray.""",
      keywords='adblocker tray system tray icon',
      url='http://githup.com/artiya4u/hblock',
      author='Artiya Thinkumpang',
      author_email='artiya4u@gmail.com',
      license='MIT',
      packages=find_packages(),
      package_data={
          'hblock.data': ['hblock.png', 'hblock-enabled.png', 'hblock-disabled.png']
      },
      install_requires=[
          'requests>=2.2.1',
      ],
      entry_points={
          'console_scripts': ['hblock = hblock:main'],
      },
      zip_safe=False)
