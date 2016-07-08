import inspect

get_sem_verbs = ['list', 'get']
post_sem_verbs = ['create']
put_sem_verbs = ['update', 'configure']
delete_sem_verbs = ['remove', 'delete', 'destroy']


def name_url(provider, cloud, method_name):
    """
    Get a URL for a method in a driver
    """
    snake_parts = method_name.split('_')
    if len(snake_parts) <= 1:
        return False

    # Convention for libcloud is ex_ are extended methods
    if snake_parts[0] == 'ex':
        extra = True
        method_name = method_name.replace('ex_', '', 1)
    else:
        extra = False
    snake_parts = method_name.split('_')
    # Try to semantically match the method name to a REST action
    if snake_parts[0] in get_sem_verbs:
        method = 'GET'
        for verb in get_sem_verbs:
            method_name = method_name.replace('%s_' % verb, '', 1)
    elif snake_parts[0] in delete_sem_verbs:
        method = 'DELETE'
    elif snake_parts[0] in put_sem_verbs:
        method = 'PUT'
    else:
        method = 'POST'

    uri = '/%s/%s/%s%s' % (provider,
                           cloud,
                           'extensions/' if extra else '',
                           method_name)
    return (method, uri)


def extract_params(method):
    """
    Extract the parameters.
    """
    return inspect.getargspec(method)
