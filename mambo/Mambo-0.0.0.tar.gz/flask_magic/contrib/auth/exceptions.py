

from flask_magic.exceptions import HTTPException


class AuthLoginNotAllowedError(HTTPException):
    code = 501
    description = "LOGIN not allowed. Contact admin if this is an error"


class AuthSignupNotAllowedError(HTTPException):
    code = 501
    description = "SIGNUP not allowed. Contact admin if this is an error"


class AuthSocialLoginNotAllowedError(HTTPException):
    code = 501
    description = "SOCIAL Login not allowed. Contact admin if this is an error"

class AuthEmailLoginRequiredError(HTTPException):
    code = 501
    description = "An Email login is required"

class AuthSociallLoginRequiredError(HTTPException):
    code = 501
    description = "A Social login is required"

