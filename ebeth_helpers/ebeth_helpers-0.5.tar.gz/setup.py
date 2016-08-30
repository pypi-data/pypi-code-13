from setuptools import setup

setup(name='ebeth_helpers',
      version='0.5',
      description='mini tools to speed up gbdx work',
      url='https://github.com/lizasapphire/gbdx_helpers',
      author='Elizabeth Golden',
      author_email='elizabeth.golden@digitalglobe.com',
      license='',
      packages=['ebeth_helpers'],
      install_requires=[
          'gbdxtools',
          'requests',
      ],
      # dependency_links=['https://sourceforge.net/projects/json-py/'],
      zip_safe=False)