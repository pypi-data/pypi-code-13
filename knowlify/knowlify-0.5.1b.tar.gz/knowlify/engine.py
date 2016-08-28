# This one decides what to do
from abc import ABCMeta, abstractproperty

import knowlify.config as config
import microserver
import os
from threading import Thread
import webbrowser


class Engine( object ):
    __metaclass__ = ABCMeta

    @abstractproperty
    def __enter__(self):
        raise NotImplementedError

    @abstractproperty
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError


class KnowlingEngine( Engine ):
    """
    Knowlifies a given html file
    """

    def __init__(self, url_or_filename):
        super( url_or_filename )

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class ChunkingEngine( Engine ):
    """
    Auto-Chunks and selects the words to knowl
    """

    def __init__(self, path):
        super( path )

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class ContextingEngine( Engine ):
    """
    Live-Contexting of links
    """

    def __init__(self, base_filepath):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class MicroServerEngine( Engine ):
    """
    Because Javascript is holding the world hostage
    """

    def __init__(self, file_path=None, port=config.MPORT, data_dir=config.DATA_DIR):
        """

        :rtype: object
        """
        self._file = file_path
        self._port = port
        self._data_dir = data_dir
        self._server = None
        self._handler = None


        self._browser = webbrowser.get(config.browser)

    def __enter__(self):
        self._old_dir = os.path.abspath( os.path.curdir )
        os.chdir( os.path.abspath( self._data_dir ) )

        self._server, self._handler = \
            microserver.start_server( self._port, self._data_dir )

        self._thread = Thread(target=self._server.serve_forever)
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self._old_dir )
        microserver.close_server(self._server)
        self._thread.join()

    def open_page(self):

        print self.web_path
        self.browser.open(self.web_path,new=1)

    @property
    def server(self):
        return self._server

    @property
    def handler(self):
        return self._handler

    @property
    def port(self):
        return self._port

    @property
    def data_directory(self):
        return self._data_dir

    @property
    def current_file(self):
        return self._file

    @property
    def browser(self):
        return self._browser

    @property
    def web_path(self):
        return 'http://127.0.0.1' + ':' + str(self._server.server_address[1]) + '/' + os.path.split(self._file)[-1]
