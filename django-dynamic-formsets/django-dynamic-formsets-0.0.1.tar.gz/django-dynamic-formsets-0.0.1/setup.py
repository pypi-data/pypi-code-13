from distutils.core import setup  # NOQA


REPO_URL = 'https://github.com/dallasmorningnews/django-dynamic-formsets'


setup(
    name='django-dynamic-formsets',
    packages=['dynamic_formsets'],
    version='0.0.1',
    description='A random test lib',
    author='Allan James Vestal, The Dallas Morning News',
    author_email='ajvestal@dallasnews.com',
    url=REPO_URL,
    download_url=REPO_URL + '/tarball/0.0.1',
    keywords=['django', 'formset', 'javascript'],
    classifiers=[],
    license='New BSD License',
    long_description=open('README.md').read(),
)
