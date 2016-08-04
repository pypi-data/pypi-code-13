from setuptools import setup
setup(name='LitleSdkPython3',
      version='9.3.1beta',
      description='Vantiv eCommerce SDK for Python',
      author='Aleksander Sukharev',
      author_email='sambademon@gmail.com',
      url='https://github.com/SambaDemon/litle-sdk-for-python',
      packages=['litleSdkPython'],
      install_requires=[
                        'PyXB==1.2.4',
                        'paramiko==1.14.0',
                        'requests==2.10.0'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: Information Technology',
          'License :: OSI Approved :: MIT License',
          'Operating System :: Microsoft',
          'Operating System :: Unix',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Office/Business :: Financial',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      )
