from setuptools import setup


setup(name='aiohipchat',
      version='0.0.1',
      description='Simple bot that plugs into aiohttp and HipChat',
      author='Matt Rasband',
      author_email='matt.rasband@gmail.com',
      maintainer='Matt Rasband',
      maintainer_email='matt.rasband@gmail.com',
      license='Apache-2.0',
      url='https://github.com/mrasband/aiohipchat',
      download_url='https://github.com/mrasband/aiohipchat/archive/v0.0.1.tar.gz',
      keywords=['asyncio', 'hipchat', 'bot', 'chatbot'],
      py_modules=['aiohipchat'],
      classifiers=[
          'Programming Language :: Python :: 3.5',
          'License :: OSI Approved :: Apache Software License',
          'Intended Audience :: Developers',
          'Development Status :: 4 - Beta',
      ],
      install_requires=['aiohttp'])
