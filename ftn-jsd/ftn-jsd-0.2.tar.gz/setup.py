from setuptools import setup

setup(name='ftn-jsd',
      version='0.2',
      description='Generate some Django and Play code',
      url='https://github.com/ftn-tim2/jsd-project.git',
      author='FTN',
      author_email='ftn@ftn.com',
      license='MIT',
      packages=['generated'],
      package_dir={
            'generated': 'src/generated'
      },
      package_data={
            'generated': [
                              'templates/django_templates/apps/*',
                              'templates/django_templates/assets/css/*',
                              'templates/django_templates/assets/fonts/LigatureSymbols/*',
                              'templates/django_templates/assets/img/*',
                              'templates/django_templates/assets/js/vendor/*',
                              'templates/django_templates/database/*',
                              'templates/django_templates/necessary_files/*',
                              'templates/django_templates/program/templates/class_html/*',
                              'templates/django_templates/program/templates/registration/*',
                              'templates/django_templates/program/templates/*.tx',
                              'templates/django_templates/program/*.tx',
                              'model/*.tx',
                              'model/*.rbt',
                              ],
      },
      install_requires=[
      		'Arpeggio==1.2.1',
      		'Jinja2==2.8',
      		'MarkupSafe==0.23',
      		'Pillow==3.3.1',
      		'pydot',
      		'pyparsing==2.0.6',
      		'textX==0.4.2',
      		'Unipath==1.1'
      ],
      include_package_data=True,
      zip_safe=False)