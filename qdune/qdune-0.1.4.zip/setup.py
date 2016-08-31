from setuptools import setup


setup(name='qdune',
      version='0.1.4',
      description='dune point cloud processing tools',
      author='Thomas Ashley',
      author_email='tashley22@gmail.com',
      url='https://github.com/tashley/qDune',
      license='MIT',
      packages=['qdune'],
      include_package_data=True,
      install_requires = ['numpy', 'pandas', 'statsmodels', 'matplotlib']
)
