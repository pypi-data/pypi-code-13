from pip.req import parse_requirements
from setuptools import find_packages
from setuptools import setup
from setuptools.command.install import install as _install


install_requirements = parse_requirements('requirements.txt', session=False)
requirements = [str(ir.req) for ir in install_requirements]


class install(_install):

    def run(self):
        _install.run(self)


setup(
    name='d-clean',
    version='0.0.4',
    author=u'Alexander Brandstedt',
    author_email='alexanderbrandstedt@gmail.com',
    download_url='https://github.com/qoneci/d-clean',
    description='Docker clean script',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'd-clean=d_clean.cli:cli',
        ]},
    cmdclass={'install': install},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
        ],
    )
