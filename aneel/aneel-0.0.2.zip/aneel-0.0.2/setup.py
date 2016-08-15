# -*- coding: utf-8 -*-
import setuptools
import textwrap

setuptools.setup(
    name="aneel",
    version="0.0.2",
    url="https://github.com/renatoefsousa/ANEEL",
    license="MIT License",
    author="Renato Eduardo Farias de Sousa",
    author_email="renato.ef.sousa@gmail.com",
    long_description=textwrap.dedent("""\
            (Very short) Tutorial
            =====================
            First create a Github instance::
                from github import Github
                g = Github("user", "password")
            Then play with your Github objects::
                for repo in g.get_user().get_repos():
                    print repo.name
                    repo.edit(has_wiki=False)
            You can also create a Github instance with an OAuth token::
                g = Github(token)
            Or without authentication::
                g = Github()
            Reference documentation
            =======================
            See http://pygithub.github.io/PyGithub/v1/index.html"""),
    keywords="aneel cálculos regulamentos",
    description=u"This package performs various calculations related to ANEEL regulations.",
    packages=["aneel"],
    install_requires=["csv", "json"],
)
