from setuptools import find_packages
from setuptools import setup

long_description = '''\
django-image-diet is a Django application for removing unnecessary bytes from image
files.  It optimizes images without changing their look or visual quality
("losslessly").

It works on images in JPEG, GIF and PNG formats and will leave others
unchanged. Provides a seemless integration with easy_thumbnails app, but can
work with others too.'''

setup(
    author="Arabel.la",
    author_email='geeks@arabel.la',
    name='django-image-diet',
    version='0.1.4.2',
    description='Remove unnecessary bytes from images',
    long_description=long_description,
    url='https://github.com/ArabellaTech/django-image-diet',
    platforms=['OS Independent'],
    license='MIT License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'Topic :: Utilities',
    ],
    install_requires=[
        'django>=1.8, <1.9',
    ],
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False
)
