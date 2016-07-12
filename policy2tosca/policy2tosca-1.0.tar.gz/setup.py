from distutils.core import setup
setup(
  name = 'policy2tosca',
  packages = ['policy2tosca'], # this must be the same as the name above
  include_package_data=True,
  version = '1.0',
  description = 'Policy injection module',
  author = 'Shiva Charan M S',
  author_email = 'shiva-charan.m-s@hpe.com',
  url = 'https://gerrit.opnfv.org/gerrit/parser', # use the URL to the github repo
  classifiers = [],
)
