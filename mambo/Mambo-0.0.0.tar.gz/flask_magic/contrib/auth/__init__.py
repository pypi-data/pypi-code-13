import functools
import flask_login
from flask_login import current_user
from flask import current_app
from flask_magic import register_app, get_config, abort, mail, url_for, views, models
from flask_magic import utils
from flask_magic.exceptions import AppError
from . import model
import dateutil

register_app(__package__)


def setup(**kw):
    # Setup the db here
    model.setup(**kw)

# ------------------------------------------------------------------------------

ROLES_ADMIN = ["SUPERADMIN", "ADMIN"]
ROLES_MANAGER = ROLES_ADMIN + ["MANAGER"]
ROLES_CONTRIBUTOR = ROLES_MANAGER + ["EDITOR", "CONTRIBUTOR"]
ROLES_CONTRIBUTOR = ROLES_CONTRIBUTOR + ["MODERATOR"]


def _get_app_options():
    c = get_config("INSTALLED_APPS")
    return c[__name__]["options"] if __name__ in c else {}


def is_authenticated():
    """ A shortcut to check if a user is authenticated """
    return current_user.is_authenticated


def not_authenticated():
    """ A shortcut to check if user not authenticated."""
    return not is_authenticated()


def email_reset_password(user_login):
    """
    To reset a user password and send email
    :param user_login: UserLogin object
    :return:
    """
    if user_login.login_type != models.AuthUserLogin.TYPE_EMAIL:
        raise AppError("Invalid login type. Must be the type of email to be sent email to")

    options = _get_app_options()
    delivery = options.get("reset_password_method") or "token"
    token_ttl = get_config("reset_password_token_ttl") or 60
    email_template = options.get("reset_password_email_template") or "reset-password.txt"
    new_password = None

    if delivery.lower() == "token":
        token = user_login.set_temp_login(token_ttl)
        url = url_for(views.AuthLogin.reset_password, token=token, _external=True)
    else:
        new_password = user_login.change_password(random=True)
        url = url_for(views.AuthLogin.index, _external=True)

    mail.send(template=email_template,
              method_=delivery.lower(),
              to=user_login.email,
              name=user_login.user.name,
              email=user_login.email,
              url=url,
              new_password=new_password)


def _create_user_login_verify_email(user_login):
    if user_login.login_type != models.AuthUserLogin.TYPE_EMAIL:
        raise AppError("Invalid login type. Must be the type of email to be sent email to")

    options = _get_app_options()
    token_ttl = options.get("verify_email_token_ttl") or (60 * 24)
    token = user_login.set_email_verified_token(token_ttl)
    url = url_for(views.AuthLogin.verify_email, token=token, _external=True)
    return token, url


def email_verification_email(user_login):
    if user_login.login_type != models.AuthUserLogin.TYPE_EMAIL:
        raise AppError("Invalid login type. Must be the type of email to be sent email to")

    options = _get_app_options()
    email_template = options.get("verify_email_template") or "verify-email.txt"
    token, url = _create_user_login_verify_email(user_login)

    mail.send(template=email_template,
              to=user_login.email,
              name=user_login.user.name,
              email=user_login.email,
              verify_url=url)


def email_signup_welcome(user_login):
    if user_login.login_type != models.AuthUserLogin.TYPE_EMAIL:
        raise AppError(
            "Invalid login type. Must be the type of email to be sent email to")

    options = _get_app_options()
    verify_email = options.get("verify_email") or False
    email_template = options.get("verify_signup_email_template") or "verify-signup-email.txt"
    token, url = _create_user_login_verify_email(user_login)

    mail.send(template=email_template,
              to=user_login.email,
              name=user_login.user.name,
              email=user_login.email,
              verify_url=url,
              verify_email=verify_email)


# ---------------------- DECORATORS --------------------- #

def authenticated(func):
    """
    A wrapper around the flask_login.login_required.
    But it also checks the presence of the decorator: @unauthenticated
    On a "@authenticated" class, method containing "@unauthenticated" will
    still be able to access without authentication
    :param func:
    :return:
    """
    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        if "unauthenticated" not in utils.get_decorators_list(func) \
                and not_authenticated():
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view


def unauthenticated(func):
    """
    Dummy decorator. @authenticated will inspect the method
    to look for this decorator
    Use this decorator when you want do not require login in a "@authenticated" class/method
    :param func:
    :return:
    """
    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        return func(*args, **kwargs)
    return decorated_view


def logout_user(f):
    """
    Decorator to logout user
    :param f:
    :return:
    """
    @functools.wraps(f)
    def deco(*a, **kw):
        flask_login.logout_user()
        return f(*a, **kw)
    return deco


def require_email_verified(f):
    pass


def require_login_allowed(f):
    """
    Decorator to abort if login is not allowed
    :param f:
    :return:
    """
    @functools.wraps(f)
    def deco(*a, **kw):
        if not _get_app_options().get("allow_login"):
            abort("AuthLoginNotAllowedError")
        return f(*a, **kw)
    return deco


def require_signup_allowed(f):
    """
    Decorator to abort if signup is not allowed
    :param f:
    :return:
    """
    @functools.wraps(f)
    def deco(*a, **kw):
        if not _get_app_options().get("allow_signup"):
            abort("AuthSignupNotAllowedError")
        return f(*a, **kw)
    return deco


def require_social_login_allowed(f):
    """
    Decorator to abort if social login is not allowed
    :param f:
    :return:
    """
    @functools.wraps(f)
    def deco(*a, **kw):
        if not _get_app_options().get("allow_social_login"):
            abort("AuthSocialLoginNotAllowedError")
        return f(*a, **kw)
    return deco


def accepts_roles(*roles):
    """
    A decorator to check if user has any of the roles specified

    @roles_accepted('superadmin', 'admin')
    def fn():
        pass
    """
    def wrapper(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            if is_authenticated():
                if not current_user.has_any_roles(*roles):
                    return abort(403)
            else:
                return abort(401)
            return f(*args, **kwargs)
        return wrapped
    return wrapper


def accepts_admin_roles(func):
    """
    Decorator that accepts only admin roles
    :param func:
    :return:
    """
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        return accepts_roles(*ROLES_ADMIN)(func)(*args, **kwargs)
    return decorator


def accepts_manager_roles(func):
    """
    Decorator that accepts only manager roles
    :param func:
    :return:
    """
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        return accepts_roles(*ROLES_MANAGER)(func)(*args, **kwargs)
    return decorator


def accepts_contributor_roles(func):
    """
    Decorator that accepts only contributor roles
    :param func:
    :return:
    """
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        return accepts_roles(*ROLES_CONTRIBUTOR)(func)(*args, **kwargs)
    return decorator


def accepts_moderator_roles(func):
    """
    Decorator that accepts only moderator roles
    :param func:
    :return:
    """
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        return accepts_roles(*models.ROLES_MODERATOR)(func)(*args, **kwargs)
    return decorator

