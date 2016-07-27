from setuptools import setup, find_packages

setup(
    name = 'app',
    version = '0.0.1',
    keywords = ('bee', 'egg'),
    description = 'a simple egg',
    license = 'MIT License',

    url = 'http://liluo.org',
    author = 'HalShaw',
    author_email = 'xiaohaogreat@qq.com',

    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [],
)