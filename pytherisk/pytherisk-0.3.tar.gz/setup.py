from setuptools import setup

try:
    long_description = open('README.md').read()
except IOError:
    long_description = ''

setup(
	name='pytherisk',
	version='0.3',
    url='https://github.com/lucascudo/pytherisk.git',
	scripts=['pytherisk.py'],
    keywords=["asterisk", "AMI", "AGI", "voice", "google", "speak"],
    install_requires=[
        "gTTS"
    ]
)