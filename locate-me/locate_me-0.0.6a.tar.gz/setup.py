from setuptools import setup, find_packages

setup(

    name="locate_me",
    version="0.0.6a",
    description="Python CLI tool that returns hidden GPS coordinates from photos and locates it on a google map",
    url="https://github.com/Zabanaa/locate-me",
    author="Karim Cheurfi",
    author_email="karim.cheurfi@gmail.com",
    license="WTFPL",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Graphics :: Capture :: Digital Camera',
        'Programming Language :: Python :: 3'
    ],
    keywords="exif data gps info google maps",
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=['requests', 'googlemaps', 'pillow'],
    entry_points={
        'console_scripts': [
            'locate_me=locate_me:main'
        ]
    }
)
