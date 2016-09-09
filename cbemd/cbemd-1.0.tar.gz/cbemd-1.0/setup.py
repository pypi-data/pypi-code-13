from distutils.core import setup, Extension

setup(
    name='cbemd',
    version='1.0',
    ext_modules = [
        Extension(
            'cbemd',
            include_dirs = ['.'],
            sources = ['pyemd.c', 'cbemd.c'],
            extra_compile_args = ['-g']
        )
    ],
    scripts = ['cbemd.h'],
    author = "cb modified slightly from Andreas Jansson's amazing work",
    author_email = '',
    description = ("modification of Python wrapper around Yossi Rubner's Earth Mover's Distance implementation (http://ai.stanford.edu/~rubner/emd/default.htm)"),
    license = 'GPL v3',
    keywords = 'emd distance',
)
