from setuptools import setup

setup(name='ci-jira-releaser',
      version='0.3',
      description='Simple way to release past(or current) commits within Jira',
      url='https://github.com/bookmd/jira-releaser',
      author='Ben Waters',
      author_email='ben@book-md.com',
      license='MIT',
      packages=['ci_jira_releaser'],
      install_requires=['jira', 'gitpython', 'requests'],
      scripts=['bin/ci-jira-releaser'],
      zip_safe=False)
