from distutils.core import setup
import pytz


setup(
    name='gae-pytz',
    version=pytz.__version__,
    url='https://github.com/potatolondon/gae-pytz/',
    license='MIT',
    author='Stuart Bishop',
    author_email='stuart@stuartbishop.net',
    description='A version of pytz for Django on Google App Engine.',
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['pytz'],
    include_package_data=True,
    package_data={'pytz': ['zoneinfo.zip']},
)
