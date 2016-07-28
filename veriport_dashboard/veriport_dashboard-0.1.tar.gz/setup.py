from setuptools import setup
setup(
  name = 'veriport_dashboard',
  packages = ['veriport_dashboard'], # this must be the same as the name above
  version = '0.1',
  description = 'This is a dashboard utility made specifically for Veriport project',
  author = 'Ronil Rufo',
  author_email = 'ronil.rufo@gmail.com',
  url = 'https://github.com/verifydx/veriport-dashboard', # use the URL to the github repo
  download_url = 'https://github.com/verifydx/veriport-dashboard/tarball/0.1', # I'll explain this in a second
  keywords = ['veriport', 'dashboard', 'veriport_dashboard'], # arbitrary keywords
  classifiers = [],
  install_requires=["numpy", "reportlab", "django-haystack"],
)
