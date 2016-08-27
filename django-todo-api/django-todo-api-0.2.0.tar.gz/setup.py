from setuptools import find_packages, setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='django-todo-api',
    version='0.2.0',
    description="API for managing todo's.",
    long_description=readme(),
    url='https://gitlab.com/cdriehuys/django-todo-api',
    author='Chathan Driehuys',
    author_email='cdriehuys@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    packages=find_packages(exclude=['example_project']),
    include_package_data=True,
    install_requires=[
        'django >= 1.8, < 1.11',
        'djangorestframework',
    ],
    zip_safe=False)
