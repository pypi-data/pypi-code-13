# -*- coding: utf-8 -*-
"""
    pip_services_runtime.run.ProcessRunner
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Microservice process runner implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import sys
import signal
import time
import threading

class ProcessRunner(object):

    _microservice = None
    _exit_event = None

    def __init__(self, microservice):
        self._microservice = microservice
        self._exit_event = threading.Event()

    def set_config(self, config):
        self._microservice.set_config(config)

    def load_config(self, config_path):
        self._microservice.load_config(config_path)

    def load_config_with_default(self, default_config_path):
        args = sys.argv
        config_path = args[1] if len(args) > 1 else default_config_path
        self._microservice.load_config(config_path);

    def _capture_errors(self):
        def handle_exception(exc_type, exc_value, exc_traceback):
            self._microservice.fatal(exc_value)
            self._microservice.info("Process is terminated");
            self._exit_event.set()
            #sys.exit(1)

        sys.excepthook = handle_exception

    def _capture_exit(self):
        self._microservice.info("Press Control-C to stop the microservice...")

        def sigint_handler(signum, frame):
            self._microservice.info("Goodbye!")            
            self._exit_event.set()            
            #sys.exit(1)
            
        signal.signal(signal.SIGINT, sigint_handler)
        signal.signal(signal.SIGTERM, sigint_handler)

        # Wait and close
        self._exit_event.clear()
        while not self._exit_event.is_set():
            try:
                self._exit_event.wait(1)
            except:
                pass # Do nothing...

    def run(self):
        self._capture_errors()
        self._microservice.start()
        self._capture_exit()
        self._microservice.stop()

    def run_with_config(self, config):
        self.set_config(config)
        self.run()

    def run_with_config_file(self, config_path):
        self.load_config(config_path)
        self.run()

    def run_with_default_config_file(self, default_config_path):
        self.load_config_with_default(default_config_path)
        self.run()
