from setuptools import setup

setup(
    name='lektor-css-min',
    version='0.1.1',
    author=u'Joy Chen',
    author_email='joyhzchen@gmail.com',
    url='https://github.com/joyhchen/lektor-css-min',
    license='MIT',
    py_modules=['lektor_css_min'],
    entry_points={
        'lektor.plugins': [
            'css-min = lektor_css_min:CssMinPlugin',
        ]
    },
    install_requires=['chardet', 'csscompressor']
)
