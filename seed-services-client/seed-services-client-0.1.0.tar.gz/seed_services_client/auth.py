from demands import JSONServiceClient


class AuthApiClient(object):
    """
    Client for Auth Service.

    :param str email:

        An email address.

    :param str password:

        A password.

    :param str api_url:
        The full URL of the API.

    """

    def __init__(self, email, password, api_url, session=None):
        if session is None:
            session = JSONServiceClient(url=api_url)
        # login
        data = {"email": email, "password": password}
        login = session.post('/user/tokens/', data=data)
        self.token = login["token"]
        headers = {'Authorization': 'Token %s' % self.token}
        session = JSONServiceClient(url=api_url,
                                    headers=headers)
        self.session = session

    def get_permissions(self):
        return self.session.get('/user/')
