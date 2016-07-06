from distutils.core import setup

setup(
    name='renrensdk',
    version='1.5',
    description='Renren Python3 SDK, especially for social network research.',
    long_description=open('README', 'r').read(),
    author='Luping Yu',
    author_email='lazydingding@gmail.com',
    url='https://github.com/lazydingding/renrensdk',
    download_url='https://github.com/lazydingding/renrensdk',
    license='Apache',
    platforms='any',
    py_modules=['renren'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
