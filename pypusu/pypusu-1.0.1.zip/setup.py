from distutils.core import setup

setup(
    name='pypusu',
    packages=['pypusu'],  # this must be the same as the name above
    version='1.0.1',
    description='Python client for PuSuEngine',
    author='Janne Enberg',
    author_email='janne.enberg@lietu.net',
    url='https://github.com/PuSuEngine/pypusu',
    download_url='https://github.com/PuSuEngine/pypusu/tarball/v1.0.1',
    keywords=['pubsub', 'publisher', 'subscriber', 'messaging'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "Programming Language :: Python",
        "Topic :: Communications :: Chat",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
