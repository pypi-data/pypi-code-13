# coding=utf-8
import copy
from simple_permissions.compat import six


def autodiscover(module_name=None):
    """
    Autodiscover INSTALLED_APPS perms.py modules and fail silently when not
    present. This forces an import on them to register any permissions bits
    they may want.
    """
    from django.utils.module_loading import module_has_submodule
    from simple_permissions.compat import import_module
    from simple_permissions.conf import settings

    module_name = module_name or settings.SIMPLE_PERMISSIONS_AUTODISCOVER_MODULE_NAME

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's perms module
        try:
            # discover the permission module
            discover(app, module_name=module_name)
        except:
            # Decide whether to bubble up this error. If the app just doesn't
            # have an perms module, we can just ignore the error attempting
            # to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, module_name):
                raise


def discover(app, module_name=None):
    """
    Automatically apply the permission logics written in the specified
    module.

    Examples
    --------
    Assume if you have a ``perms.py`` in ``your_app`` as::

        from simple_permissions.logics import AuthorPermissionLogic
        PERMISSION_LOGICS = (
            ('your_app.your_model', AuthorPermissionLogic),
        )

    Use this method to apply the permission logics enumerated in
    ``PERMISSION_LOGICS`` variable like:

        >>> discover('your_app')
    """
    from simple_permissions.compat import import_module
    from simple_permissions.compat import get_model
    from simple_permissions.conf import settings
    from simple_permissions.utils.logics import add_permission_logic

    variable_name = settings.SIMPLE_PERMISSIONS_AUTODISCOVER_VARIABLE_NAME
    module_name = module_name or settings.SIMPLE_PERMISSIONS_AUTODISCOVER_MODULE_NAME

    # import the module
    m = import_module('%s.%s' % (app, module_name))

    # check if the module have PERMISSION_LOGICS variable
    if hasattr(m, variable_name):
        # apply permission logics automatically
        permission_logic_set = getattr(m, variable_name)
        for model, permission_logic in permission_logic_set:
            if isinstance(model, six.string_types):
                # convert model string to model instance
                model = get_model(*model.split('.', 1))
            add_permission_logic(model, permission_logic)
