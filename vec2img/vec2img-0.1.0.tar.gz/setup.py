from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import vec2img

requires = ['numpy', 'Pillow']

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        import pytest
        pytest.main(self.test_args)

setup(
    name='vec2img',
    version=vec2img.__version__,
    description=vec2img.__description__,
    long_description=open('README.rst').read(),
    url='https://github.com/midnightSuyama/vec2img',
    author='midnightSuyama',
    author_email='midnightSuyama@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License'
    ],
    keywords='opencv vec',
    packages=find_packages(exclude=['tests*']),
    install_requires=requires,
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    entry_points={
        'console_scripts': [
            'vec2img=vec2img.command:main'
        ]
    }
)
