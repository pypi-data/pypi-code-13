from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='ci-jira-releaser',
      version='0.3.8.2',
      long_description=readme(),
      description='Simple way to release past(or current) commits within Jira',
      url='https://github.com/bookmd/jira-releaser',
      author='Ben Waters',
      author_email='ben@book-md.com',
      license='MIT',
      packages=['ci_jira_releaser'],
      install_requires=['jira', 'gitpython', 'requests'],
      scripts=['bin/ci-jira-releaser'],
      zip_safe=False)
