from setuptools import setup

setup(name='ca_tracker',
      version='0.2.11',
      description='Package for cell segmentation, tracking, classification into asc negative and asc positive cells and calcium intensity measurements over time',
      #url='http://github.com/storborg/funniest',
      author='Christoph Moehl, Image and Data Analysis Facility, German Center of Neurodegenerative Diseases, Bonn, Germany',
      author_email='christoph.moehl@dzne.de',
      #license='MIT',
      packages=['ca_tracker'],
      install_requires=['numpy', 'scipy', 'matplotlib', 'numexpr', 'bottleneck', 'six', 'pandas', 'scikit-image', 'seaborn', 'pillow', 'pims', 'trackpy'],
      include_package_data=True,
      test_suite = 'nose.collector',
      tests_require = ['nose'],
      scripts = ['bin/ca_tracker'],
      zip_safe=False)
