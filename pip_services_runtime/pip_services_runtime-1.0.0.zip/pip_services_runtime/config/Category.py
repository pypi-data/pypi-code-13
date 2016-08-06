# -*- coding: utf-8 -*-
"""
    pip_services_runtime.config.Category
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Components category enumeration
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class Category(object):
    """
    Category of components or configuration sections that are used to configure components.
    """

    Undefined = 'undefined'
    """
    Undefined category
    """

    Factories = 'factories'
    """
    Component factories
    """

    Discovery = 'discovery'
    """
    Service discovery components
    """

    Boot = 'boot'
    """
    Bootstap configuration readers
    """

    Logs = 'logs'
    """
    Logging components
    """

    Counters = 'counters'
    """
    Performance counters
    """

    Cache = 'cache'
    """
    Value caches
    """

    Persistence = 'persistence'
    """
    Persistence components
    """

    Clients = 'clients'
    """
    Clients to other microservices or infrastructure services
    """

    BusinessLogic = 'logic'
    """
    Any business logic component - controller or decorator
    """

    Controllers = 'controllers'
    """
    Business logic controllers
    """

    Decorators = 'decorators'
    """
    Decorators to business logic controllers
    """

    Services = 'services'
    """
    API Services
    """

    Addons = 'addons'
    """
    Various microservice addons / extension components
    """
