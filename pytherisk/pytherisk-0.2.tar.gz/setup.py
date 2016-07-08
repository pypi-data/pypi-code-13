from setuptools import setup

try:
    long_description = open('README.md').read()
except IOError:
    long_description = ''

setup(
	name='pytherisk',
	version='0.2',
    url='https://github.com/cascudo/pytherisk.git',
	scripts=['pytherisk.py'],
    keywords=["asterisk", "AMI", "AGI", "voice", "google", "speak"],
    install_requires=[
        "gTTS"
    ]
)