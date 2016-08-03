
class ConfigError(Exception):
    pass


class ConfigNotFoundError(ConfigError, FileNotFoundError):
    pass

