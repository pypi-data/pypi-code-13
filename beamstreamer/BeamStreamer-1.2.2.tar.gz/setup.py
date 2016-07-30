#!/usr/bin/env python3

from distutils.core import setup

setup(name="BeamStreamer",
        version="1.2.2",
        description="Watch Beam streams in VLC!",
        author="Innectic",
        author_email="no@notforyou.whatever",
        url="https://www.github.com/innectic/beam-streamer",
        packages=["beamstreamer"],
        scripts=["bstream"],
        install_requires=[
            "requests",
            "xmltodict"
            ]
        )
