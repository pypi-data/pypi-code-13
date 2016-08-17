import simplejson as json
import requests
import hashlib
import psycopg2
import datetime
import datetime
import zlib


class EventClient:
    def __init__(self, token, endpoint, source='default'):
        self.source = source
        self.endpoint = endpoint
        self.token = token

    def get_headers(self) -> dict:
        return {
            'x-api-token': self.token,
        }

    def push_event(self, event_type: str, data: dict):
        return self.push_many_events(event_type, [data])

    def push_many_events(self, event_type: str, data: list):
        for i in range(len(data)):
            data[i]['source'] = self.source

        return self.api_post_req('/type/%s/event' % event_type, data)

    def create_type(self, json_schema):
        self.api_post_req('/type', json_schema)

    def api_post_req(self, path, data):
        data = json.dumps(data)

        req = requests.post(self.endpoint + path, headers=self.get_headers(), data=data)
        if req.status_code != 201:
            raise Exception("Event storage error. Status: %s" % req.status_code)

    def get_types(self):
        req = requests.get("%s/type" % self.endpoint, headers=self.get_headers())
        return req.json()

    def delete_type(self, type_name):
        req = requests.delete("%s/type/%s" % (self.endpoint, type_name), headers=self.get_headers())

        if req.status_code != 200:
            raise Exception("Event storage error. Status: %s" % req.status_code)

    def get_db_connection(self):
        req = requests.get("%s/db" % self.endpoint, headers=self.get_headers())

        if req.status_code != 200:
            raise Exception("Event storage error. Status: %s" % req.status_code)

        return psycopg2.connect(**req.json())


class EventsLogger:
    def __init__(self, log_path: str, source: str):
        self.event_file = EventFile(log_path)
        self.source = source

    def emit(self, event_type: str, data: dict, tags: list = [], time: datetime.datetime = datetime.datetime.now()):
        """
        Add new event to datastore (file).
        """

        data['_type'] = event_type
        data['tags'] = tags
        data['datetime'] = str(time)
        data['source'] = str(self.source)

        self.event_file.write(data)


class EventFile:
    def __init__(self, log_path: str):
        self.log_path = log_path

    def write(self, data: dict):
        """
        Write dict to file (JSON + CRC)
        """
        data = json.dumps(data)
        with open(self.log_path, 'a') as f:
            f.write("%s %s\n" % (data, zlib.crc32(data.encode())))
            f.flush()

    def read_events(self):
        """
        Read events from file and validate CRC.
        Damaged records are skipped.
        """
        with open(self.log_path, 'r') as f:
            for line in f:
                last_space = line.rfind(' ')
                if int(line[last_space + 1:-1]) == zlib.crc32(line[:last_space].encode()):
                    yield json.loads(line[:last_space])
                else:
                    pass  # skip damaged records


class Pusher:
    @staticmethod
    def push_all(api_client: EventClient, event_file: EventFile):
        for event in event_file.read_events():
            event_type = event['_type']
            del event['_type']
            api_client.push_event(event_type, event)
