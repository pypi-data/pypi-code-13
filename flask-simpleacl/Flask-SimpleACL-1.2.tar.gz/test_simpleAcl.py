#flask/bin/python
import unittest
from flask import Flask, g, redirect, request
from flask_login import LoginManager, login_user
from flask_simpleAcl import ACL


class Roles(object):
    '''
    Users roles constants
    '''
    USER = 0
    ADMIN = 1


class Consts(object):
    '''
    Text constants for not repeat in tests.
    '''
    LOGIN = 'LOGIN PAGE'
    USERS = 'USERS ONLY'
    ADMINS = 'ADMIN ONLY'
    INDEX = 'NOT ALLOWED'
    GROUP = 'GROUP ALLOWED'
    OTHER_REDIRECT = 'OTHER REDIRECT PAGE'


class User():
    '''
    Mock users class
    '''
    id = 1
    login = 'test'
    password = 'test'
    role = Roles.USER

    def get_id(self):

        return self.id

    def is_active(self):
        return True

    def is_authenticated(self):
        return True


class TestApp():
    def create_app(self):
        '''
        Create test App
        :return:
        '''
        app = Flask(__name__)

        lm = LoginManager()
        lm.init_app(app)

        acl = ACL(app)
        app.config['SECRET_KEY'] = 'secret'

        @lm.user_loader
        def load_user(id):
            user = User()
            if id == 2:
                user.role = Roles.ADMIN
            return user

        @app.route('/index')
        def index():
            return Consts.INDEX

        @app.route('/other-redirect')
        def other_redirect():
            return Consts.OTHER_REDIRECT

        @app.route('/admin')
        @acl.access(access=Roles.ADMIN)
        def admin():
            return Consts.ADMINS

        @app.route('/admin-redirect')
        @acl.access(access=Roles.ADMIN, redirect='other_redirect')
        def admin_redirect():
            return Consts.ADMINS

        @app.route('/group')
        @acl.access(access=[Roles.ADMIN, Roles.USER])
        def group():
            return Consts.GROUP

        @app.route('/login')
        def login():
            return Consts.LOGIN


        @app.route('/lp', methods=['POST'])
        def lp():
            '''
            Page for login with Flask test_client().
            :return:
            '''
            user = User()

            if int(request.form['role']) == Roles.ADMIN:
                user.id = 2

            login_user(user, force=True, remember=True)
            return redirect(request.form['act'])

        return app


class AclTests(unittest.TestCase):
    def setUp(self):
        self.app = TestApp().create_app()

    def test_failGetIfNotLogined(self):
        '''
        Test get protected page without login.
        :return:
        '''
        with self.app.test_client() as client:
            response = client.get('/admin', follow_redirects=True)

        assert response.data == Consts.LOGIN

    def test_successAccessForAdmin(self):
        '''
        Test get protected page with allowed one access role.
        :return:
        '''
        response = self._getPageWithAuth('/admin', Roles.ADMIN)
        assert response.data == Consts.ADMINS

    def test_successGroupAccess(self):
        '''
        Test get protected page with allowed access group
        :return:
        '''
        response = self._getPageWithAuth('/group', Roles.ADMIN)
        assert response.data == Consts.GROUP

        response = self._getPageWithAuth('/group', Roles.USER)
        assert response.data == Consts.GROUP

    def test_redirectNotAllowed(self):
        '''
        Test redirect to default page for denied access role.
        :return:
        '''
        response = self._getPageWithAuth('/admin', Roles.USER)
        assert response.data == Consts.INDEX

    def test_redirectNotAllowedDifferentPage(self):
        '''
        Test redirect to not default 'not-access' page for denied access role.
        :return:
        '''
        response = self._getPageWithAuth('/admin-redirect', Roles.USER)
        assert response.data == Consts.OTHER_REDIRECT

    def _getPageWithAuth(self, page, role):
        '''
        Get page with login in test_client app context.

        :param page:
        :param role:
        :return:
        '''
        with self.app.test_client() as client:
            response = client.post('/lp', data={'act': page, 'role': role}, follow_redirects=True)
        return response

if __name__ == '__main__':
    unittest.main()
