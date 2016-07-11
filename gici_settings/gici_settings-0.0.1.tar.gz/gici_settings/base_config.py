from settings import Settings


class BaseConfig(object):
    def __init__(self, base_dir, env):
        self.settings = Settings(base_dir)
        self.env = env

    def get_configuration(self):
        return self.settings.load_config(config_level=self.env)
