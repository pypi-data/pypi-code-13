from setuptools import setup, find_packages


def readme():
    f = open('README.md', 'r')
    text = f.read()
    f.close()
    return text


version = '0.1'

setup(name='pydendroheatmap-kmyoo',
      version=version,
      description="Tool for creating heatmaps, where rows and columns are organized by hierarchical clusters",
      long_description="""\
Tool for creating heatmaps, where rows and columns are organized by hierarchical clusters as seen in https://github.com/themantalope/dendroheatmap, which is based onhttp://code.activestate.com/recipes/578175-hierarchical-clustering-heatmap-python/""",
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='dendroheatmap dendrogram heatmap',
      author='Kang Min Yoo',
      author_email='kaniblurous@gmail.com',
      url='https://github.com/kaniblu/dhm/',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'numpy',
          'scipy',
          'colour',
          'matplotlib',
      ],
      entry_points="",
      )
