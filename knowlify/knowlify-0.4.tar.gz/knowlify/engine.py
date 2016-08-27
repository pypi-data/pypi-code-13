# This one decides what to do
from abc import ABCMeta, abstractproperty
import os, sys



class Engine(metaclass=ABCMeta):

    @abstractproperty
    def __init__(self):
        raise NotImplementedError

    @abstractproperty
    def __enter__(self):
        raise NotImplementedError

    @abstractproperty
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError


class KnowlingEngine(Engine):
    """
    Knowlifies a given html file
    """

    def __init__(self, url_or_filename):
        super(url_or_filename)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class ChunkingEngine(Engine):
    """
    Auto-Chunks and selects the words to knowl
    """

    def __init__(self, path):
        super(path)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class ContextingEngine(Engine):
    """
    Live-Contexting of links
    """

    def __init__(self, base_filepath):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
