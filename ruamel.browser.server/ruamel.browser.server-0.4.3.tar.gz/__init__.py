# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

_package_data = dict(
    full_package_name="ruamel.browser.server",
    version_info=(0, 4, 3),
    author="Anthon van der Neut",
    author_email="a.van.der.neut@ruamel.eu",
    description="server providing decoupled browser creation/driving via zmq",
    # keywords="",
    license="MIT License",
    entry_points='rbs=ruamel.browser.server.__main__:main',
    since=2013,
    status=u"β",  # the package status on PyPI
    install_requires=dict(
        any=["ruamel.appconfig", "ruamel.std.argparse", "pyzmq", "pyvirtualdisplay", ],
    ),
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet :: WWW/HTTP",
    ],
)


def _convert_version(tup):
    """Create a PEP 386 pseudo-format conformant string from tuple tup."""
    ret_val = str(tup[0])  # first is always digit
    next_sep = "."  # separator for next extension, can be "" or "."
    for x in tup[1:]:
        if isinstance(x, int):
            ret_val += next_sep + str(x)
            next_sep = '.'
            continue
        first_letter = x[0].lower()
        next_sep = ''
        if first_letter in 'abcr':
            ret_val += 'rc' if first_letter == 'r' else first_letter
        elif first_letter in 'pd':
            ret_val += '.post' if first_letter == 'p' else '.dev'
    return ret_val

version_info = _package_data['version_info']
__version__ = _convert_version(version_info)

del _convert_version
