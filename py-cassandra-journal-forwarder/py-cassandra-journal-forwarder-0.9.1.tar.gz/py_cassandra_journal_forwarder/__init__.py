#! /usr/bin/python2

import re
import time
import yaml
import select
import datetime

from systemd import journal
from os.path import expanduser
from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement

def main():
    settings = load_settings()
    cluster = Cluster(contact_points=settings.contact_points, port=settings.port)
    session = cluster.connect(keyspace=settings.keyspace)
    cursor = Cursor(settings)
    cur_pos = '' 
    while cursor.poll.poll():
        if cursor.journal.process() != journal.APPEND:
            continue
        for entry in cursor.journal:
            if entry["MESSAGE"] != "" and entry["__CURSOR"] != cur_pos:
                query, cur_pos = build_insert_from_log({key.strip('_'): entry[key] for key in entry.keys()}, settings)
                if query:
                    try:
                        session.execute(query)
                        cursor.update_cursor(cur_pos)
                    except Exception:
                        print("failed uploading journal entry")


def build_insert_from_log(data, settings):
    cols , values = [], []
    for k, v in data.iteritems(): # iterate over Json returned by journal
        if k not in ['LIMIT', 'MONOTONIC_TIMESTAMP']: # this is a hack, please remove
            if k == 'CURSOR': # if value is _CURSOR assign it to a varaible to save our position
                cursor = v
            elif k in ['SYSTEMD_SESSION', 'SESSION_ID', 'SYSLOG_FACILITY']: # Fix for ubuntu
                v = str(v)
                if k == 'SYSLOG_FACILITY':
                    v = v.replace("'", "''")
            if v.__class__ == 'uuid.UUID': # if value is a UUID, convert it to a usable format
                v = v.get_bytes()
            elif type(v) == datetime.datetime: # if value is a timestamp, remove microseconds and TZ offset
                v = str(v).split('.')[0]
            elif type(v) == unicode: # if value is a string/unicode replace single quotes with double single quotes to avoid query format issues
                v = v.replace("'", "''")
            cols.append(k)
            values.append(str(v) if type(v) == int else "'{}'".format(v))
    if len(cols) > 0 and len(values) > 0:
        query = SimpleStatement(
                "insert into {} ({}) values({})".format(
                    settings.table,
                    joined(cols),
                    joined(values)), consistency_level=ConsistencyLevel.ONE)
        return query, cursor
 

def joined(strings):
    return ', '.join(strings)


def load_settings():
    settings_path = expanduser('~') + '/.config/cassandra-journal-forwarder/settings.yaml'
    try:
        with open(settings_path, 'r') as file:
            settings = yaml.load(file)
        parsed_settings = Settings(**settings)
        return parsed_settings
    except Exception:
        print('no settings file found in path: {}'.format(settings_path))
        exit()

class Settings(object):
    def __init__(self, cassandra, cursor_file):
        self.contact_points = cassandra['contact_points']
        self.port = cassandra['port']
        self.keyspace = cassandra['keyspace']
        self.table = cassandra['table']
        self.cursor_file = str(cursor_file).format(home=expanduser('~'))


class Cursor(object):
    def __init__(self, settings):
        self.journal = journal.Reader()
        self.cursor_file = settings.cursor_file
        self.iterations = 0
        # load current cursor position
        try:
            with open(self.cursor_file, 'r') as f:
                cursor = f.read()
                print("resuming from: {}".format(cursor))
                self.journal.seek_cursor(cursor)
        except Exception:
            print("no cursor file found, starting as far back in the logs as possible")
        self.poll = select.poll()
        self.poll.register(self.journal,self.journal.get_events())

    def update_cursor(self, position):
        self.iterations += 1
        if self.iterations > 100:
            with open(self.cursor_file, 'w+') as f:
                print('saving position: {}'.format(position))
                f.write(position)
                self.iterations = 0

if __name__ == '__main__':
    main()
