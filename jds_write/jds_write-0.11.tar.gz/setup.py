from setuptools import setup

setup(name='jds_write',
      version='0.11',
      description='The funniest joke in the world',
      url='http://github.com/despiegj/jds_write',
      author='Jan De Spiegeleer',
      author_email='jds@riskconcile.com',
      license='MIT',
      packages=['jds_write'],
      install_requires=[
          'nbconvert','nbformat','jinja2'],
      include_package_data=True,
      zip_safe=False)
