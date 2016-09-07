from __future__ import print_function

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

from collections import namedtuple
import json

from .bearing import Bearing
from .point import Point


Wind = namedtuple('Wind', ['direction', 'speed', 'relative_direction'])


class Boatd(object):
    def __init__(self, host='localhost', port=2222):
        '''
        Create a boat instance, connecting to boatd at `host` on port `port`
        '''
        self.host = host
        self.port = port

    def url(self, endpoint):
        '''Return a formatted url pointing at `endpoint` on the boatd server'''
        return 'http://{0}:{1}{2}'.format(self.host, self.port, endpoint)

    def get(self, endpoint):
        '''Return the result of a GET request to `endpoint` on boatd'''
        json_body = urlopen(self.url(endpoint)).read().decode('utf-8')
        return json.loads(json_body)

    def post(self, content, endpoint=''):
        '''
        Issue a POST request with `content` as the body to `endpoint` and
        return the result.
        '''
        url = self.url(endpoint)
        post_content = json.dumps(content).encode('utf-8')
        headers = {'Content-Type': 'application/json'}
        request = Request(url, post_content, headers)

        response = urlopen(request)

        return json.loads(response.read().decode('utf-8'))

    def quit(self):
        content = self.post({'quit': True}, '/')
        print(content)

    @property
    def version(self):
        '''Return the version of boatd'''
        content = self.boatd.get('/')
        return content.get('boatd').get('version')


class Boat(object):
    '''A boat controlled by boatd'''

    def __init__(self, boatd=None):
        if boatd is None:
            self.boatd = Boatd()
        else:
            self.boatd = boatd

    @property
    def heading(self):
        '''
        Return the current heading of the boat in degrees.

        :returns: current bearing
        :rtype: Bearing
        '''
        content = self.boatd.get('/boat')
        return Bearing(float(content.get('heading')))

    @property
    def wind(self):
        '''
        Return the direction of the wind in degrees.

        :returns: wind object containing direction bearing and speed
        :rtype: Wind
        '''
        content = self.boatd.get('/wind')
        return Wind(
            Bearing(content.get('direction')) - self.heading,
            content.get('speed'),
            Bearing(content.get('direction'))
        )

    @property
    def relative_wind(self):
        '''
        Return the direction of the wind, relative to the boat's current
        direction.

        :returns: wind direction bearing in boat coordinates
        :rtype: Bearing
        '''
        return self.wind.direction

    @property
    def position(self):
        '''
        Return the current position of the boat.

        :returns: current position
        :rtype: Point
        '''
        content = self.boatd.get('/boat')
        lat, lon = content.get('position')
        return Point(lat, lon)

    def set_rudder(self, angle):
        '''
        Set the angle of the rudder to be `angle` degrees.

        :param angle: rudder angle
        :type angle: float between -90 and 90
        '''
        angle = float(angle)
        request = self.boatd.post({'value': float(angle)}, '/rudder')
        return request.get('result')

    def set_sail(self, angle):
        '''
        Set the angle of the sail to `angle` degrees

        :param angle: sail angle
        :type angle: float between -90 and 90
        '''
        angle = float(angle)
        request = self.boatd.post({'value': float(angle)}, '/sail')
        return request.get('result')


class Behaviour(object):
    def __init__(self, boatd=None):
        if boatd is None:
            self.boatd = Boatd()
        else:
            self.boatd = boatd

    def _get_behaviour_data(self):
        return self.boatd.get('/behaviours')

    def list(self):
        '''Return a list of the available behaviours to run.'''
        return list(self._get_behaviour_data().get('behaviours').keys())

    def start(self, name):
        '''
        End the current behaviour and run a named behaviour.

        :param name: the name of the behaviour to run
        :type name: str
        '''
        d = self.boatd.post({'active': name}, endpoint='/behaviours')
        current = d.get('active')
        if current is not None:
            return 'started {}'.format(current)
        else:
            return 'no behaviour running'

    def stop(self):
        '''
        Stop the current behaviour.
        '''
        self.start(None)


def get_current_waypoints(boatd=None):
    '''
    Get the current set of waypoints active from boatd.

    :returns: The current waypoints
    :rtype: List of Points
    '''

    if boatd is None:
        boatd = Boatd()

    content = boatd.get('/waypoints')
    return [Point(*coords) for coords in content.get('waypoints')]


def get_home_position(boatd=None):
    '''
    Get the current home position from boatd.

    :returns: The configured home position
    :rtype: Points
    '''

    if boatd is None:
        boatd = Boatd()

    content = boatd.get('/waypoints')
    home = content.get('home', None)
    if home is not None:
        lat, lon = home
        return Point(lat, lon)
    else:
        return None


if __name__ == '__main__':
    boat = Boat()
    print(boat.version)
    print(boat.heading)
    print(boat.wind)
    print(boat.position)
    print(boat.rudder(0))
    print(boat.rudder(10))
