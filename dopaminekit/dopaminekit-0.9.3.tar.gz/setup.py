from setuptools import setup

version = '0.9.3'

setup(name='dopaminekit',
      packages = ['dopaminekit'],
      version=version,
      description="A library to use DopamineLabs machine learning API",
      long_description="""\
This packages provides a class for interacting with the DopamineAPI from a python project. After you have received your API key and configured the actions and reinforcements relevant to your app on the [Dopamine Developer Dashboard](dashboard.usedopamine.com), you may use this class to place 'tracking()', and 'reinforcement()' calls from inside your app that will communicate directly with the machine learning based DopamineAPI.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='machinelearning analytics dopamine reinforcement behavior',
      author='Akash Desai',
      author_email='kash@usedopamine.com',
      url='https://github.com/DopamineLabs/DopamineKit-Python-Client',
      download_url='https://github.com/DopamineLabs/DopamineKit-Python-Client/tarball/'+version,
      license='MIT',
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
)