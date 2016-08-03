from setuptools import setup
from setuptools import find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='dss',
      version='0.7',
      description='Defense Support System',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Natural Language :: English',
        'Topic :: Security',
        'Topic :: System :: Logging',
        'Topic :: System :: Archiving',
        'Topic :: System :: Monitoring',
        'Environment :: Plugins',
      ],
      keywords='dss defense support system security logging archiving monitoring plugin architecture',
      url='https://github.com/ostrovskis/core',
      author='UTEP Software Engineering Practicum Summer 2016',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'python-xlib',
          'dpkt',
          'autopy',
          'psutil',
          'schedule',
          'configobj',
          'netifaces',
      ],
      scripts=['bin/dss-gui', 'bin/dss-shell'],
      include_package_data=True,
      zip_safe=False)