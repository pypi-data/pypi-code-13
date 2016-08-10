from setuptools import setup, find_packages

setup(name="slack_jirer",
    version="1.0",
    description="Slack JIRA URL expander",
    classifiers=[
        "Programming Language :: Python",
    ],
    author="Nikola Kotur",
    author_email="kotnick@gmail.com",
    url="https://github.com/kotnik/slack-jirer",
    download_url="https://github.com/kotnik/slack-jirer/archive/1.0.zip",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "slackbot",
        "jira",
    ],
    entry_points={
        "console_scripts": [
            'slack_jirer = slack_jirer.main:main',
        ],
    },
)
