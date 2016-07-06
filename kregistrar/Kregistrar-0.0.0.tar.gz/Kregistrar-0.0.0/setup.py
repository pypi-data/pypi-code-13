from setuptools import setup


setup(
    name='Kregistrar',
    version='0.0.0',
    packages=['Kregistrar'],
    url='https://github.com/adatao/Kregistrar',
    author='Arimo, Inc.',
    author_email='info@arimo.com',
    description='Monitor of training progress of Deep Learning models built on TensorFlow & Theano',
    long_description='Monitor of training progress of Deep Learning models built on TensorFlow & Theano',
    license='MIT License',
    install_requires=['Theano', 'Keras', 'Bokeh'],
    classifiers=[],
    keywords='Deep Learning Keras Tensorflow Theano')
