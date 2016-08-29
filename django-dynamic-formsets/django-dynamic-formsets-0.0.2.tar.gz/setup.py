from distutils.core import setup  # NOQA


REPO_URL = 'https://github.com/dallasmorningnews/django-dynamic-formsets'

VERSION = '0.0.2'


setup(
    name='django-dynamic-formsets',
    packages=['dynamic_formsets'],
    version=VERSION,
    description='A random test lib',
    author='Allan James Vestal, The Dallas Morning News',
    author_email='ajvestal@dallasnews.com',
    url=REPO_URL,
    download_url=REPO_URL + '/tarball/' + VERSION,
    keywords=['django', 'formset', 'javascript'],
    classifiers=[],
    license='New BSD License',
    long_description=open('README.md').read(),
)
