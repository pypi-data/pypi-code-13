from distutils.core import setup
long_description = 'mp4 rotation angle: read and set'
with open('README.rst') as file:
    long_description = file.read()

setup(name='qtrotate',
      version='2.1.7',
      url='https://github.com/evgenity/qtrotate',
      author='evgenity',
      author_email='evgenity.dev@gmail.com',
      py_modules=['qtrotate'],
      description = 'mp4 rotation angle: read and set',
      long_description=long_description,
      )
