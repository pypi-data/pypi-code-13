import logging
import os

from search_engine_app.Settings.Settings import Settings


class Trace:

    _logger = None
    _LOG_FORMAT = u'[%(asctime)s]\ttID:%(thread)d\t\tfunc:%(funcName)s - file:%(filename)s:%(lineno)d\t\t\t%(message)s'
    _FILE_MODE_NEW ='w'
    _FILE_MODE_APPEND ='a'
    _cur_file_mode = _FILE_MODE_APPEND
    _does_initialized = False
    _TRACE_MODE_FILE ='file'
    _TRACE_MODE_CONSOLE ='console'
    _DEFAULT_TRACE_NAME ='debug.trace'
    _LOGGER_NAME ='Trace'

    @staticmethod
    def _initialize():
        if not Trace._does_initialized:
            mode = Settings.getTraceMode()
            if mode == Trace._TRACE_MODE_FILE:
                Trace._enable_debug_trace_to_file()
            elif mode == Trace._TRACE_MODE_CONSOLE:
                Trace._enable_debug_trace_to_console()
            Trace._logger = logging.getLogger(Trace._LOGGER_NAME)
            Trace._does_initialized = True

    @staticmethod
    def _getTracePath():
        log_path = Settings.getTraceFile()
        if not os.path.realpath(log_path):
            logging.error('Wrong trace path:{0} .'.format(log_path))

        if log_path == None:
            cur_dir = os.path.dirname(__file__)
            default_log_path = os.path.join(cur_dir, Trace._DEFAULT_TRACE_NAME)
            logging.error('Default trace path defined:{0} .'.format(default_log_path))
            log_path = default_log_path
        return log_path



    @staticmethod
    def _enable_debug_trace_to_file():
        Trace._require_new_debug_trace_file()
        log_path = Trace._getTracePath()
        Trace._logger = logging.getLogger(Trace._LOGGER_NAME)
        hdlr = logging.FileHandler(log_path,Trace._cur_file_mode)
        formatter = logging.Formatter(Trace._LOG_FORMAT)
        hdlr.setFormatter(formatter)
        Trace._logger.addHandler(hdlr)
        Trace._logger.setLevel(logging.DEBUG)

    @staticmethod
    def _require_new_debug_trace_file():
        Trace._cur_file_mode = Trace._FILE_MODE_NEW


    @staticmethod
    def _enable_debug_trace_to_console():
        logging.basicConfig(level=logging.DEBUG,format=Trace._LOG_FORMAT,filemode=Trace._cur_file_mode)

    @staticmethod
    def thread_trace(message):
        Trace._initialize()
        Trace._logger.debug(message)

