from setuptools import setup, find_packages


setup(
    name="soulmates_app_common",
    version='0.1',
    description='common utils modules etc',
    include_package_data = True,
    
    # Author details
    author='Eddy Lazar',
    author_email='eddy.lazar@soulmates.pro',
    license='MIT',
    packages=find_packages(exclude=['migrations', 'docs', 'tests']),
    
    # install_requires=[
#         'django>1.9, <2.0',
#         'cloudinary==1.4.0',
#     ],
    install_requires=[
        'django >1.9, <2.0',
        'cloudinary==1.4.0',
    ],
)