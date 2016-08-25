from setuptools import setup

setup(name='insight360mlapi',
      version='0.12',
      description='API to call trained model stored in Azure ML portal to predict building energy',
      url='',
      author='Runsheng Song',
      author_email='runsheng.song@autodesk.com',
      license='MIT',
      packages=['insight360mlapi'],
      install_requires=[
        'gbXMLParser>=0.65'
    ],
      zip_safe=False)