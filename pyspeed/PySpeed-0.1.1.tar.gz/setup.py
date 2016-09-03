from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(
    # Package info
    name         = "PySpeed",
    version      = "0.1.1",
    description  = "PySpeed - flexible progress bars for Python",
    license      = "MIT/X11",
    url          = "https://launchpad.net/pyspeed",
    #download_url = "",
    #classifiers  = ["",]
    author       = "Rani Hod",
    #author_email = "",
    maintainer   = "Amit Aronovitch",
    maintainer_email = "pyspeed-dev@lists.launchpad.net",
    platforms = ["any"],
    long_description = """\
Time flies when you're having fun!

Add progress bars to your program with easy to use, Pythonic,
wrapper iterators.
Supports multi-level bars, text-mode bars (for the terminal),
and graphical ones (GTK).
""",
    #
    extras_require = {
        'gprogress': ["PyGTK > 2.12.1"],
        },
    #tests_require = ["PyGTK > 2.12.1"],
    #
    packages = find_packages(),
    )
