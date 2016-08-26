from setuptools import setup, find_packages

setup(
    name='placeholders',
    version='0.7',
    packages=find_packages(),
    description='Create placeholder images by embedding keywords into regular jpg images.',
    author='Austin Brown',
    author_email='austinbrown34@gmail.com',
    url='https://github.com/austinbrown34/placeholders',
    download_url='https://github.com/austinbrown34/placeholders/tarball/0.7',
    keywords=['image', 'exif', 'jpg'],
    py_modules=['placeholders', 'placeholder_tools'],
    classifiers=[],
    install_requires=[
        'Click',
        'pyyaml',
        'piexif'
    ],
    entry_points='''
        [console_scripts]
        placeholders=placeholders:make_placeholders
    ''',
)
