import requests
from django.conf import settings


def _url(path):
    return ''


class Client(object):
    """
    Encapsulates all the logic to consume the services provided
    by the balystic API.
    """
    AUTH_ENDPOINT = 'authenticate/'
    USER_ENDPOINT = 'users/'
    BLOG_ENDPOINT = 'blog/'
    QA_ENDPOINT = 'qa/'

    def __init__(self):
        """
        Token should be provided by the admin of the community.
        Root must be the full path to the api root
        i.e. http://sample.7dhub.com/api/
        """
        self.headers = {'Authorization': 'TOKEN '+settings.BALYSTIC_API_TOKEN}
        self.root = settings.BALYSTIC_API_PATH

    def _make_request(self, path, method, data=None):
        """
        Encapsulates error handling. Sets an standard way to handle
        requests across the client.
        Path should end with slash.
        """
        if method == 'GET':
            request_method = requests.get
        elif method == 'POST':
            request_method = requests.post
        elif method == 'DELETE':
            request_method = requests.delete
        full_path = self.root + path
        try:
            response = request_method(full_path, headers=self.headers, data=data)
            return response.json()
        except requests.exceptions.MissingSchema:
            return {'error': 'The supplied API endpoint is missing the schema'}
        except requests.exceptions.ConnectionError:
            return {'error': 'Cannot communicate with server'}
        except requests.exceptions.Timeout:
            return {'error': 'Server is not responding'}

    def get_users(self):
        """
        Retrieves the list of users in the community.
        There are two kind of users, owners and regular users.
        """
        return self._make_request(self.USER_ENDPOINT, 'GET')

    def get_user_detail(self, username):
        """
        Retrieves an user detail.
        The user must be in the community for this to work.
        """
        return self._make_request(
            self.USER_ENDPOINT + username + '/', 'GET')

    def delete_user(self, username):
        """
        Removes an user from the community.
        """
        return self._make_request(
            self.USER_ENDPOINT + username + '/', 'DELETE')

    def add_user(self, username):
        """
        Adds an user to the community.
        """
        return self._make_request(
            self.USER_ENDPOINT + username + '/', 'POST')

    def get_blogs(self, page=1):
        """
        Retrieves the list of blog posts in the community
        """
        return self._make_request(
            self.BLOG_ENDPOINT + '?page=' + str(page), 'GET')

    def get_blog_detail(self, slug):
        """
        Retrieves a blog post detail
        """
        return self._make_request(
            self.BLOG_ENDPOINT + slug + '/', 'GET')

    def get_questions(self, page=1):
        """
        retrieves the list of questions on a
        community
        """
        return self._make_request(
            self.QA_ENDPOINT + '?page=' + str(page), 'GET')

    def create_question(self, data):
        """
        creates a question
        """
        return self._make_request(
            self.QA_ENDPOINT, 'POST', data=data)

    def get_question_detail(self, pk):
        """
        Retrieves a blog post detail
        """
        return self._make_request(
            self.QA_ENDPOINT + pk + '/', 'GET')

    def create_answer(self, pk, data):
        """
        Retrieves a blog post detail
        """
        return self._make_request(
            self.QA_ENDPOINT + pk + '/', 'POST', data=data)

    def authenticate_user(self, email, password):
        """
        Verifies the credentials of an user and returns
        True or False depending on the outcome.
        """
        data = {'email': email, 'password': password}
        response = self._make_request(
            self.AUTH_ENDPOINT, 'POST', data)
        return 'username' in response.keys()
