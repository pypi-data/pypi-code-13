from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template, TemplateDoesNotExist

from common_dibbs.config.configuration import Configuration


class ClientAuthenticationBackend(object):
    def authenticate(self, username=None, password=None, session_key=None):
        from common_dibbs.clients.cas_client.apis.authentication_api import AuthenticationApi

        # Create a client for Authentication
        operations_client = AuthenticationApi()
        operations_client.api_client.host = "%s" % (Configuration().get_central_authentication_service_url(),)

        result = operations_client.authenticate_post(**{
            "username": username,
            "password": password,
            "session_key": session_key,
        })

        user = None
        if result.response:
            user = User()
            user.username = result.username

        return {
            "user": user,
            "token": result.token
        }

default_redirect_form_value = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Redirection to authentication server</title>
</head>
<body>
    <form id="redirect_form" action="{{ cas_service_target_url }}" method="POST">
        <input type="hidden" name="session_key" value="{{ session_key }}">
        <input type="hidden" name="redirect_url" value="{{ redirect_url }}">
        <button type="submit">You will be redirected to the authentication server</button>
    </form>
</body>
</html>
"""

class CentralAuthenticationMiddleware(object):
    def process_request(self, request):
        username = request.META.get('X_USERNAME')
        password = request.META.get('X_PASSWORD')
        session_key = request.session.session_key

        auth_backend = ClientAuthenticationBackend()

        # Check if the current session has already been authenticated by the CAS: authentication is successful
        authentication_resp = auth_backend.authenticate(username, password, session_key)

        if authentication_resp["user"] is not None and authentication_resp["user"].username not in ["", "anonymous"]:
            request.user = authentication_resp["user"]
            return

        # Do a web redirection to the CAS service
        redirect_url = "http://%s%s" % (request.META.get('HTTP_HOST'), request.path)
        cas_service_target_url = "%s" % (Configuration().get_central_authentication_service_url(), )

        data = {
            "request": request,
            "session_key": session_key,
            "redirect_url": redirect_url,
            "cas_service_target_url": cas_service_target_url
        }

        try:
            t = get_template("redirect_form.html")
        except TemplateDoesNotExist:
            t = Template(default_redirect_form_value)

        c = Context(data)
        html_source = str(t.render(c))

        # Redirection via a form
        return HttpResponse(html_source)

LOGGED_USERS = {

}
