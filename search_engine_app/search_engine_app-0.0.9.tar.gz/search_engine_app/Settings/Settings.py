import configparser
import os


class Settings:
    SETTINGS_FILE_NAME = 'settings.ini'
    _config = None
    _path = None

    @staticmethod
    def getPathToFile():
        if Settings._path == None:
            dir = os.path.dirname(__file__)
            path = os.path.join(dir, Settings.SETTINGS_FILE_NAME)
            Settings.setPathToFile(path)
        return Settings._path

    @staticmethod
    def setPathToFile(path):
        Settings._config = None
        Settings._path = path

    @staticmethod
    def _initialize():
        if Settings._config == None:
            log_path = Settings.getPathToFile()
            Settings._config = configparser.ConfigParser()
            Settings._config.read(log_path)

    @staticmethod
    def _get(name, section='app_settings'):
        try:
            Settings._initialize()
            value = Settings._config.get(section, name)
        except Exception as e:
            value = None
        return value

    @staticmethod
    def getTraceFile():
        '''
        @return: pathToTraceFile
        '''
        return Settings._get('trace_file')

    @staticmethod
    def getTraceMode():
        '''
        @return: traceMode [file | console | none]
        '''
        return Settings._get('trace_mode')

    @staticmethod
    def getThreadPoolCapacity():
        return Settings._get('threads_pool_cpacity')

    @staticmethod
    def getAppMode():
        '''
        @return: appMode [PRODUCTION | DEBUG]
        '''
        return Settings._get('app_mode')

    @staticmethod
    def getAppLogFile():
        '''
        @return: appLogFilePath
        '''
        return Settings._get('app_log_file')
