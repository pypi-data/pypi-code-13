from distutils.core import setup

setup(
    name='pypusu',
    packages=['pypusu'],  # this must be the same as the name above
    version='1.0.0b',
    description='Python client for PuSuEngine',
    author='Janne Enberg',
    author_email='janne.enberg@lietu.net',
    url='https://github.com/PuSuEngine/pypusu',
    download_url='https://github.com/PuSuEngine/pypusu/tarball/v1.0.0',
    keywords=['pubsub', 'publisher', 'subscriber', 'messaging'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
    ],
)
