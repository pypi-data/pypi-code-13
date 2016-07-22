from setuptools import setup


def readme():
    with open('README.Md') as f:
        return f.read()

setup(name='vibe',
      version='1.2.0',
      description='Python Package for Vibe, Fastest way to know everything about your contacts',
      long_description=readme(),
      author='Sachin Philip Mathew',
      url="https://github.com/sachinvettithanam/vibe",
      keywords='vibe',
      author_email='sachinvettithanam@gmail.com',
      license='MIT',
      packages=['vibe'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
