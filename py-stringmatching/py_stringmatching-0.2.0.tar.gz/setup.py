import subprocess
import sys
import os

# check if pip is installed. If not, raise an ImportError
PIP_INSTALLED = True

try:
    import pip
except ImportError:
    PIP_INSTALLED = False

if not PIP_INSTALLED:
    raise ImportError('pip is not installed.')

def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)

# check if setuptools is installed. If not, install setuptools
# automatically using pip.
install_and_import('setuptools')

# make sure numpy is installed, as we need numpy to compile the C extensions.
# If numpy is not installed, automatically install it using pip.
install_and_import('numpy')

def generate_cython():
    cwd = os.path.abspath(os.path.dirname(__file__))
    print("Cythonizing sources")
    p = subprocess.call([sys.executable, os.path.join(cwd,
                                                      'build_tools',
                                                      'cythonize.py'),
                         'py_stringmatching'],
                        cwd=cwd)
    if p != 0:
        raise RuntimeError("Running cythonize failed!")

if __name__ == "__main__":

    no_frills = (len(sys.argv) >= 2 and ('--help' in sys.argv[1:] or
                                         sys.argv[1] in ('--help-commands',
                                                         'egg_info', '--version',
                                                         'clean')))

    cwd = os.path.abspath(os.path.dirname(__file__))
    if not os.path.exists(os.path.join(cwd, 'PKG-INFO')) and not no_frills:
        # Generate Cython sources, unless building from source release
        generate_cython()

    # specify extensions that need to be compiled
    extensions = [setuptools.Extension("py_stringmatching.similarity_measure.cython_levenshtein",
                                       ["py_stringmatching/similarity_measure/cython_levenshtein.c"],
                                       include_dirs=[numpy.get_include()])]

    # find packages to be included. exclude benchmarks.
    packages = setuptools.find_packages(exclude=["benchmarks"])

    with open('README.rst') as f:
        LONG_DESCRIPTION = f.read()

    setuptools.setup(
        name='py_stringmatching',
        version='0.2.0',
        description='Python library for string matching.',
        long_description=LONG_DESCRIPTION,
        url='https://sites.google.com/site/anhaidgroup/projects/py_stringmatching',
        author='UW Magellan Team',
        author_email='uwmagellan@gmail.com',
        license='BSD',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'Intended Audience :: Education',
            'License :: OSI Approved :: BSD License',
            'Operating System :: POSIX',
            'Operating System :: Unix',
            'Operating System :: MacOS',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Topic :: Scientific/Engineering',
            'Topic :: Utilities',
            'Topic :: Software Development :: Libraries',
        ],
        packages=packages,
        install_requires=[
            'numpy >= 1.7.0',
            'six'
        ],
        ext_modules=extensions,
        include_package_data=True,
        zip_safe=False
    )

