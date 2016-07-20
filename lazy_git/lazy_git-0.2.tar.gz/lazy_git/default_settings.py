class DefaultConfig(object):
    DEBUG = False
    CSRF_ENABLED = True
    URL_PREFIX = '/api'
    REPO_DIR = '~/.lazy_git'

class ProductionConfig(DefaultConfig):
    REPO_DIR = '/var/lazy_git'

class DevelopmentConfig(DefaultConfig):
    DEBUG = True

class TestingConfig(DefaultConfig):
    pass
