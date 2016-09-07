from setuptools import setup

setup(
    name='send_ses_message',
    version='0.1.2',
    packages=['send_ses_message'],
    scripts=['ses_smtp_mailer.py'],
    license='MIT',

    package_data={
        'send_ses_message': ['examples/*.cfg'],
    },
    author='Edward J. Stronge',
    author_email='ejstronge@gmail.com',
    url="https://github.com/ejstronge/send_ses_message/",
    download_url="https://github.com/ejstronge/send_ses_message/tarball/0.1.1",
    description='Send email using the Amazon SES IMAP interface',
    keywords='aws ses email',
)
