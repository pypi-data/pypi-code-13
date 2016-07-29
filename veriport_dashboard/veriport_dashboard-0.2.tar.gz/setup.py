from setuptools import setup, find_packages
setup(
    name = 'veriport_dashboard',
    include_package_data=True,
    package_data={
        'migrations': ["*"],
        'static': ["*"],
        'templates': ["*"],
        'templatetags': ["*"]
    },
    packages=find_packages(exclude=["dist"]),
    version = '0.2',
    description = 'This is a dashboard utility made specifically for Veriport project',
    author = 'Ronil Rufo',
    author_email = 'ronil.rufo@gmail.com',
    url = 'https://github.com/verifydx/veriport-dashboard', # use the URL to the github repo
    download_url = 'https://github.com/verifydx/veriport-dashboard/tarball/0.1', # I'll explain this in a second
    keywords = ['veriport', 'dashboard', 'veriport_dashboard'], # arbitrary keywords
    classifiers = [],
    install_requires=["numpy", "reportlab", "django-haystack"],
)
