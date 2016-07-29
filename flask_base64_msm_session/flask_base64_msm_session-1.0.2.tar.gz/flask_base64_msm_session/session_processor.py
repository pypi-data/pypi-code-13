from msm_api import MemorySessionAPI
from flask.sessions import SessionMixin, SessionInterface
import uuid

class Session(dict, SessionMixin):

    def __init__(self, session_id):
        self.__id = session_id

    def get_id(self): return self.__id

class MemcachedSessionProcessor(object):

    def __init__(self, hosts):
        self.__mem_session_api = MemorySessionAPI( hosts )

    def open_session(self, app, request):
        session_cookie_name = app.session_cookie_name
        session_id = request.cookies.get(session_cookie_name)

        if session_id:
            data = self.__mem_session_api.get_user_data(session_id)
            session = Session(session_id)
            session.update(data)
        else:
            session = Session(uuid.uuid1().hex.upper())

        return session

    def save_session(self, app, session, response):
        session_id = session.get_id()
        self.__mem_session_api.update_user_data(session_id, session)
        response.set_cookie(app.session_cookie_name, session_id)

    def is_null_session(self, session):
        return False


