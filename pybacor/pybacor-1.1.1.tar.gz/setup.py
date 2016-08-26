from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='pybacor',
	  version='1.1.1',
	  description='ibacor API for Python',
	  long_description=readme(),
	  url='http://github.com/yanwarsolah/pybacor',
	  author='Yanwar Solahudin',
	  author_email='yanwarsolah@gmail.com',
	  license='MIT',
	  packages=['pybacor', 'pybacor.api'],
	  install_requires=[
          'requests',
      ],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
		'Natural Language :: English',
      	'Intended Audience :: Developers',
      ],
      include_package_data=True,
	  zip_safe=False)