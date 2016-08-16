from setuptools import setup, find_packages
setup(
    name = "automationapi",
    version = "0.2",
    packages = find_packages(),
    author = 'Rahul R',
    author_email = 'rsmrahul@gmail.com',
    description = 'Automation Library',
    long_description='Api for automation',
    url = 'https://github.com/rsmrahul1/automation-api', # The URL to the github repo
    download_url = 'https://github.com/rsmrahul1/automation-api.git',
    license='MIT',# Choose your license
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. 
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
        ]
    )
