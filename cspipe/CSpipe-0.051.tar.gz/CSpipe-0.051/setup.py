import ast
from distutils.core import setup
from setuptools import setup, find_packages

def get_version(fname):
    with open(fname) as f:
        source = f.read()
    module = ast.parse(source)
    for e in module.body:
        if isinstance(e, ast.Assign) and \
                len(e.targets) == 1 and \
                e.targets[0].id == '__version__' and \
                isinstance(e.value, ast.Str):
            return e.value.s
    raise RuntimeError('__version__ not found')

setup(name = 'CSpipe',  
      version = get_version('CSpipe/CSpipe'),
      keywords = 'ChIP-Seq pipe',
      description = 'ChIP-Seq pipe', 
      long_description = 'ChIP-Seq pipe',
      license = 'GPLv3',
      classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Programming Language :: Python :: 2.7',
      ],
      author = 'Yingxiang Li',  
      author_email = 'xlccalyx@gmail.com', 
      maintainer = 'Yingxiang Li',
      url = 'https://pypi.python.org/pypi/CSpipe',
      download_url = 'https://pypi.python.org/pypi/CSpipe',
      packages = ['CSpipe'],
      package_dir = {'CSpipe': 'CSpipe'},
      scripts = ['CSpipe/CSpipe'],
      package_data = {'CSpipe': ['example.input.tab', 'MarkDuplicates.jar']}
) 

