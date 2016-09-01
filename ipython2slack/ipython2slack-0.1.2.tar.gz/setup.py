from distutils.core import setup

setup(
    name='ipython2slack',
    version='0.1.2',
    description='Sending infromation fron IPython console to Slack chanel',
    long_description='',
    url='https://github.com/xfox/ipython2slack',
    author='Ivan Lazarev',
    author_email='ilazarev@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=[
        'ipython2slack',
    ],
    install_requires=[
        'ipython',
        'slackclient',
    ],
)