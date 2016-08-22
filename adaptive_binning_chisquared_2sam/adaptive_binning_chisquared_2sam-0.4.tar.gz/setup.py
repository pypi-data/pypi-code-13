from setuptools import setup

setup(name='adaptive_binning_chisquared_2sam',
      version='0.4',
      description='This repository contains a 2 sample chi squared test the uses adaptive binning using the approach of Roederer et al. (http://onlinelibrary.wiley.com/doi/10.1002/1097-0320(20010901)45:1%3C47::AID-CYTO1143%3E3.0.CO;2-A/epdf)',
      url='https://github.com/weissercn/adaptive_binning_chisquared_2sam',
      author='Constantin Weisser',
      author_email='weissercn@gmail.com',
      license='MIT',
      packages=['adaptive_binning_chisquared_2sam'],
      install_requires=[
          'numpy',
          'scipy'
      ],
      zip_safe=False)
