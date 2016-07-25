from setuptools import setup

setup(
    name="mssup",
    version="1.0.1",
    packages=['mssup'],
    package_data={
    },
    author="berry",
    author_email="iberryful@gmail",
    description="A simple tool to upload file to meituan object bucket.",
    license="MIT lisence",
    entry_points="""
    [console_scripts]
    mssup = mssup.mssup:main
    """,
    url='https://github.com/iberryful/mssup',
    install_requires={
        'mssapi': ['mssapi'],
        'click': ['click'],
    },
)
