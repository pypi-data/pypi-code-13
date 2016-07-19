# coding=utf-8


class Settings(object):

    secret_key = ''
    debug = False
    mongodb_uri = 'mongodb://localhost:27017'
    mongodb_database = 'test'
    modules = []
    tornado_application_kwargs = {
        'template_path': '',
        'static_path': '',
    }
