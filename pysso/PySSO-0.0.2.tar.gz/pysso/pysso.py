import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import time
import json
import threading
import uuid
import logging
import pymysql
from urllib.parse import urlparse
from urllib.parse import urlencode
import pysso.setting as setting
import pysso.user as user
import pysso.auth as auth

static_path = os.path.join(os.path.dirname(__file__), "static")
template_path = os.path.join(os.path.dirname(__file__), "template")

print( 'static_path:%s'%static_path )

tornado_settings = {
    'debug' : True,
    'static_path' : static_path,
    'cookie_secret' : 'aaaaaaaaaaaaaaa'
}

pretty_json_dump = lambda x:json.dumps( x,sort_keys=True,indent=4,ensure_ascii=False )

config = None
def get_config(  ):
    return config

def set_config( value ):
    global config
    config = value

def get_db_conn():
    config = get_config()
    conn = pymysql.connect(host = config['database']['host'],\
                           user = config['database']['user'],\
                           passwd = config['database']['password'],\
                           db = config['database']['db'],\
                           charset = 'utf8',\
                           cursorclass = pymysql.cursors.DictCursor)
    return conn

def sql_query_one( sql, args = []):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute( sql,args )
    value = cursor.fetchone()
    return value

def need_auth( fn ):
    def wrapper( self, *args, **kwargs ):
        user_id = self.get_secure_cookie( 'user_id' )
        if user_id == None:
            raise tornado.web.HTTPError(400)

        return fn( self, *args, **kwargs )
        
    return wrapper

class IndexHandle(tornado.web.RequestHandler):
    def get(self):
        self.redirect('/dashboard',status=302)

class LoginHandle(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8") 
        user = self.get_argument('user')
        password = self.get_argument('password')
        #ToDo: add password hash

        value = sql_query_one( 'select * from user where name=%s and password=%s',(user, password) )

        if value != None:
            ret = {'ret':'success'}
            self.set_secure_cookie( 'user_id', str(value['id']), expires_days=None )
        else:
            ret = {'ret':'failed', 'msg':'user and password not match'}

        self.write( pretty_json_dump(ret) )

class LogoutHandle(tornado.web.RequestHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect('/dashboard',status=302)
        
class DashboardHandle(tornado.web.RequestHandler):
    def get(self):
        render_args = {}
        conn = get_db_conn()
        render_args['system_name'] = setting.get( conn, setting.SET_SYSTEM_NAME )
        self.render( os.path.join( template_path, "dashboard.html"), **render_args )

class AppHandle(tornado.web.RequestHandler):
    @need_auth
    def get(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8") 
        sql = 'select name,title,description from app'
        conn = get_db_conn()
        cursor = conn.cursor()
        cursor.execute( sql )
        value = cursor.fetchall()
        
        self.write( pretty_json_dump(value) )

class GoHandle(tornado.web.RequestHandler):
    @need_auth
    def get(self, app_name):
        user_id = self.get_secure_cookie( 'user_id' ).decode('utf8')
        user = sql_query_one( 'select * from user where id=%s',(user_id,) )
        app = sql_query_one( 'select entry_url,secret from app where name=%s',(app_name,) )

        print( 'user [%s] go to app [%s]'%(user_id, app_name) )
        url_object = urlparse( app['entry_url'] )
        uri = url_object.path
        go_args = {}
        go_args['app'] = app_name
        go_args['time'] = str(int(time.time()))
        go_args['user'] = user['email']
        go_args = auth.sign('GET', uri, go_args, app['secret'])
        
        query_str = urlencode( go_args )
        target_url = app['entry_url'] + '?' + query_str
        print('redirect to:%s'%target_url)

        self.redirect( target_url )


application = tornado.web.Application([
    ("/", IndexHandle),
    ("/login", LoginHandle),
    ("/logout", LogoutHandle),
    ("/dashboard", DashboardHandle),
    ("/app", AppHandle),
    ("/go/([^/]+)",GoHandle)
],**tornado_settings)

def start_server():

    logging.basicConfig()
    logging.root.setLevel(logging.INFO)
    
    config = get_config()
    application.listen( config['port'], address=config['bind_ip'] )
    tornado.ioloop.IOLoop.instance().start()
