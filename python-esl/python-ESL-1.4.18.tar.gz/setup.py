from setuptools import setup, Extension


setup(
    name='python-ESL',
    version='1.4.18',
    author='FreeSWITCH Developers',
    description='FreeSWITCH Event Socket Library for Python',
    url='https://github.com/sangoma/python-ESL',
    download_url='https://github.com/sangoma/python-ESL/tarball/1.4.18',
    ext_modules=[
        Extension(
            '_ESL',
            sources=['esl.c',
                     'esl_buffer.c',
                     'esl_config.c',
                     'esl_event.c',
                     'esl_json.c',
                     'esl_threadmutex.c',
                     'esl_oop.cpp',
                     'ESL.i'],
            swig_opts=['-classic', '-c++', '-DMULTIPLICITY',
                       '-threads', '-I.'],
            extra_compile_args=['-I.']
        )
    ],
    py_modules=["ESL"]
)
