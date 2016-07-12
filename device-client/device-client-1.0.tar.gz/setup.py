from setuptools import setup, find_packages

setup(
      name='device-client',
      version='1.0',
      description='Radware devices python client based on vDirect',
      author='Avishay Balderman',
      author_email='avishayb@radware.com',
      url='https://www.radware.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      install_requires=['requests'],
      classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ]
)