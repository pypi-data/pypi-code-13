from setuptools import setup, find_packages
import os

long_description = open('README.rst').read()

setup(name='alembic_pastedeploy',
      version='0.0.2',
      description="Let alembic read pastedeploy-flavored ini config files.",
      long_description=long_description,
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Database :: Front-Ends',
        'Framework :: Paste',
        ],
      keywords='',
      author='Moriyoshi Koizumi',
      author_email='mozo@mozo.jp',
      url='https://github.com/moriyoshi/alembic-pastedeploy',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='alembic_pastedeploy.tests',
      install_requires=[
          'setuptools',
          'alembic',
          'pastedeploy',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      alembic_pastedeploy = alembic_pastedeploy:main
      """,
      )

