import setuptools

setup_params = dict(
    name='yg.thumpy',
    use_scm_version=True,
    author='YouGov, Plc.',
    author_email='dev@yougov.com',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires = [
        'pillow==3.2.0',
        'boto==2.1.0',
        'gevent==0.13.6',
        'pyyaml==3.10',
    ],
    setup_requires=[
        'setuptools_scm',
    ],
    entry_points = {
        'console_scripts': [
            'thumpy = thumpy:run',
        ],
    },
    url='https://github.com/yougov/yg.thumpy',
    description=(
        'A Python web server that uses Pillow to dynamically scale, '
        'crop, transform and serve images from S3 or the local '
        'filesystem'
    ),
    long_description=open('README.rst').read(),
)

if __name__ == '__main__':
    setuptools.setup(**setup_params)
