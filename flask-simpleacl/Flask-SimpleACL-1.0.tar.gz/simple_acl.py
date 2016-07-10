from flask import current_app, redirect, url_for
from functools import wraps
from flask_login import current_user
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class ACL(object):
    """
    Simple ACL extension.
    """
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('ROLE_COLUMN', 'role')
        app.config.setdefault('LOGIN_PAGE', 'login')
        app.config.setdefault('REDIRECT_IF_NOT_ALLOW', 'index')
        app.config.setdefault('ACL_DEFAULT_ROLE', 1)

    def access(self, **options):
        """
        Check access function.

        :param options: Access options
                        :access: list or roles or single role id.
                        :redirect: redirect if not allow.
        :return:
        """
        def _notAuth():
            """
            Return auth status.

            :return:
            """
            return current_user is None or not current_user.is_authenticated

        def _dontAccess(role):
            """
            Check access for all roles in list.

            :param role:
            :return:
            """
            try:
                return getattr(current_user, current_app.config['ROLE_COLUMN']) != role
            except:
                return True

        def _accessRole():
            return current_app.config['ACL_DEFAULT_ROLE'] if not 'access' in options else options['access']

        def _rdrUrl():
            """
            Return url for redirect.

            :return:
            """
            return current_app.config['REDIRECT_IF_NOT_ALLOW'] if not 'redirect' in options else options['redirect']

        def _rolesToList():
            """
            Create roles list for single role in options.

            :return:
            """
            if not isinstance(_accessRole(), list):
                options['access'] = [_accessRole()]

        def decorator(function):
            @wraps(function)
            def decorated(*args, **kwargs):
                if _notAuth():
                    return redirect(url_for(current_app.config['LOGIN_PAGE']))

                _rolesToList()
                goods = 0
                for role in options['access']:
                    if not _dontAccess(role):
                        goods += 1
                        break;

                if goods == 0:
                    return redirect(url_for(_rdrUrl()))

                ctx = function(*args, **kwargs)
                if ctx is None:
                    ctx = {}
                elif not isinstance(ctx, dict):
                    return ctx

                return function(*args, **kwargs)
            return decorated
        return decorator
