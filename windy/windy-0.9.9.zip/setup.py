from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='windy',
    version='0.9.9',
    packages = find_packages(),
    entry_points={
        "console_scripts": ['windy = windy.gui.application:main'],
        'gui_scripts': ['windy = windy.gui.application:main', ]
        },
    description='windy is Windows GUI application for managing user/system environment variables.',
    long_description=long_description,
    url='http://github.com/zeljko-m-gavrilovic/windy',
    author='bigNumbers',
    author_email='zeljko.m.gavrilovic@gmail.com',
    license='MIT',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Desktop Environment",
        "License :: Freeware",
        "Topic :: Utilities"
      ],
    keywords=["windows", "environment", "variables", "path", "developer"],
    zip_safe=False
    )
