from setuptools import setup

with open('README.md') as f:
    Readme = f.read()

with open('LICENSE') as f:
    License = f.read()

install_requires = [
    "requests"
]

setup(
    name='PyWechatAPI',
    version='0.0.3',
    description='WeChat Develop Python API',
    long_description=Readme,
    author='CaoKe',
    author_email='hitakaken@gmail.com',
    url='https://github.com/hitakaken/PyWechatAPI.git',
    license=License,
    platforms=["any"],
    packages=['wechat'],
    # test_suite="test.tests",
    install_requires=install_requires,
    # tests_require=['nose'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    data_files=[('', ['README.md'])]
)
