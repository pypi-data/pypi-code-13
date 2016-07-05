#!usr/env/bin python
import threading
from .observer import Observer

lock = threading.Lock()
database = None


def database_creator():
    """make sure you have only one instance of Database

    :return: DataBase's instance
    """
    global database
    if database is None:
        database = Database()
    return database


class Database(Observer):
    def __init__(self):
        super().__init__()
        self.data = []

    def append_data(self, data):
        lock.acquire()
        index = len(self.data)
        data['index'] = index
        self.data.append(data)
        self.notify(data)
        lock.release()
