from distutils.core import setup

setup(
    name='PACbayesianNMF',
    version='0.1.0',
    author='Astha Gupta',
    author_email='astha736@gmail.com',
    packages=['pacbayesiannmf'],
    keywords = "PAC-Bayesian Non-Negative Matrix Factorization Quasi-Bayesian Block Gradient Descent",
    license='GPLv3',
    description='Implementing NMF with PAC Bayesian apprach using block gradient descent',
    long_description=open('README.txt').read(),
    install_requires=[
        "numpy >= 1.11.0",
    ],
    classifiers = [ 'Programming Language :: Python :: 2.7']
)
