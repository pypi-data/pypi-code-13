import sys
import mysql.connector


class Database:
    host = None
    database = None
    user = None
    password = None
    port = None

    def __init__(self):
        pass

    @classmethod
    def setup(cls, host=None, database=None, user=None, password=None, port=None):
        cls.host = host
        cls.database = database
        cls.user = user
        cls.password = password
        cls.port = port

    @classmethod
    def connector(cls):
        error = ""
        if cls.host is None:
            error = "invalid database host name"
        elif cls.database is None:
            error = "invalid database name"
        elif cls.user is None:
            error = "invalid database user name"
        elif cls.password is None:
            error = "invalid database password"

        if error != "":
            print(error)
            sys.exit(1)
        else:
            return mysql.connector.connect(
                host=cls.host,
                database=cls.database,
                user=cls.user,
                password=cls.password,
                port=cls.port
            )