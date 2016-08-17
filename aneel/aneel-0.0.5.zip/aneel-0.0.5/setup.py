# -*- coding: utf-8 -*-
import setuptools
import textwrap

setuptools.setup(
    name="aneel",
    version="0.0.5",
    url="https://github.com/renatoefsousa/ANEEL",
    license="MIT License",
    author="Renato Eduardo Farias de Sousa",
    author_email="renato.ef.sousa@gmail.com",
    long_description=textwrap.dedent("""\
            (Very short) Tutorial
            =====================
            First create a variable::
                my_consumer = CompensationContinuityConsumer()
            Adjust the class parameters::
                my_consumer.set_features("abc", 2005, "BT", "URB", "INT", 327, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                             [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                             [40, 42, 43, 44, 45, 56, 47, 38, 49, 40, 51, 62])
            Then write the result::
                print(my_consumer)
            Reference documentation
            =======================
            See https://github.com/renatoefsousa/ANEEL"""),
    keywords="aneel cálculos regulamentos",
    description=u"This package performs various calculations related to ANEEL regulations.",
    install_requires=["csv", "json"],
)
