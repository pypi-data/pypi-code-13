from django.apps import apps


def is_model_registered(app_label, model_name):
    """Checks whether a given model is registered.

    This is used to only register models if they aren't
    overridden by the application

    """
    try:
        apps.get_registered_model(app_label, model_name)
    except LookupError:
        return False
    else:
        return True
