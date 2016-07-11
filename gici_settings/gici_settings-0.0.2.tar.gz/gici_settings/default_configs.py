from base_config import BaseConfig
from gici_settings.enviornments import *


class DevelopmentConfig(BaseConfig):
    def __init__(self, base_dir):
        super(DevelopmentConfig, self).__init__(base_dir, DEVELOPMENT)


class ProductionConfig(BaseConfig):
    def __init__(self, base_dir):
        super(ProductionConfig, self).__init__(base_dir, PRODUCTION)
