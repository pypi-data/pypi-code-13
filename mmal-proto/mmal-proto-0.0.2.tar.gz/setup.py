from setuptools import setup, find_packages

setup(
    name             = "mmal-proto",
    description      = "Meteorological Middleware Application Layer protobuf bindings",
    url              = "https://github.com/hodgesds/mmbal-proto/python",
    version          = "0.0.2",
    author           = "Daniel Hodges",
    author_email     = "hodges.daniel.scott@gmail.com",
    scripts          = [],
    install_requires = [ "grpcio", "protobuf" ],
    test_suite       = "",
    tests_require    = [],
    packages         = find_packages(
        where        = '.',
        exclude      = ('tests*', 'bin*'),
    ),
)
