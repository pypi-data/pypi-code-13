from setuptools import setup
import os

#os.chdir(os.path.dirname(__file__) or '.')

#scripts = ["pybot"] # bin/pybot"]
#if os.name == "nt":
#    scripts += ["bin/pybot.bat"]

setup(
    name='Twitch-Pybot',
    description='A twitch bot with a web interface',
    author='John Iannandrea',
    author_email='jiannandrea@gmail.com',
    url='http://github.com/isivisi/pybot',
    install_requires=[
        'tornado',
        'requests'
    ],
    package_data = {
        "pybot" : ["web/Chart.min.js",
                         "web/css/*",
                         "web/images/*",
                         "web/templates/*"]
    },
    include_package_data=True,
    version='0.0.1',
    packages=['pybot', "pybot/web", "pybot/globals", "pybot/filters", "pybot/features", "pybot/data"],
    zip_safe=False,
    license='GNU',
    keywords='bot twitch web interface',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'pybot = pybot:main'
        ]
    }
)