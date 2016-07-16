"""
Support for GPSD.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/gpsd/
"""
import logging
from datetime import timedelta

import voluptuous as vol

import homeassistant.util as util
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import (
    track_point_in_utc_time, track_utc_time_change)
from homeassistant.util import dt as dt_util
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (ATTR_LATITUDE, ATTR_LONGITUDE, CONF_ELEVATION)

REQUIREMENTS = ['gps3==0.33.2']

DOMAIN = "gpsd"
ENTITY_ID = "{}.gps".format(DOMAIN)

CONF_HOST = 'host'
CONF_PORT = 'port'
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 2947

ATTR_GPS_TIME = 'gps_time'
ATTR_ELEVATION = 'elevation'
ATTR_SPEED = 'speed'
ATTR_CLIMB = 'climb'
ATTR_FIX = 'fix'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_HOST): cv.string,
        vol.Optional(CONF_PORT): cv.string,
    }),
}, extra=vol.ALLOW_EXTRA)

_LOGGER = logging.getLogger(__name__)


def is_on(hass, entity_id=None):
    """Test if the sun is currently up based on the statemachine."""
    entity_id = entity_id or ENTITY_ID

    return hass.states.is_state(entity_id, "")


def next_setting(hass, entity_id=None):
    """Local datetime object of the next sun setting."""
    utc_next = next_setting_utc(hass, entity_id)

    return dt_util.as_local(utc_next) if utc_next else None


def next_setting_utc(hass, entity_id=None):
    """UTC datetime object of the next sun setting."""
    entity_id = entity_id or ENTITY_ID

    state = hass.states.get(ENTITY_ID)

    try:
        return dt_util.parse_datetime(
            state.attributes[STATE_ATTR_NEXT_SETTING])
    except (AttributeError, KeyError):
        # AttributeError if state is None
        # KeyError if STATE_ATTR_NEXT_SETTING does not exist
        return None


def next_rising(hass, entity_id=None):
    """Local datetime object of the next sun rising."""
    utc_next = next_rising_utc(hass, entity_id)

    return dt_util.as_local(utc_next) if utc_next else None


def next_rising_utc(hass, entity_id=None):
    """UTC datetime object of the next sun rising."""
    entity_id = entity_id or ENTITY_ID

    state = hass.states.get(ENTITY_ID)

    try:
        return dt_util.parse_datetime(state.attributes[STATE_ATTR_NEXT_RISING])
    except (AttributeError, KeyError):
        # AttributeError if state is None
        # KeyError if STATE_ATTR_NEXT_RISING does not exist
        return None


def setup(hass, config):
    """Track the state of the sun."""
    conf = config[DOMAIN]
    host = util.convert(conf.get(CONF_HOST), str, DEFAULT_HOST)
    port = util.convert(conf.get(CONF_PORT), str, DEFAULT_PORT)
    #hass.states.set('gpsd.GPSD', "TEST")

    platform_config = config.get(DOMAIN, {})
    gpsd = Gpsd(hass, host, port)

    gpsd.point_in_time_listener(dt_util.utcnow())

    return True


class Gpsd(Entity):
    """Representation of a GPS receiver available via GPSD."""

    entity_id = ENTITY_ID

    def __init__(self, hass, host, port):
        """Initialize the GPSD."""
        from gps3 import gps3

        self.hass = hass
        self._host = host
        self._port = port
        _LOGGER.error("GPSD service initialised")
        self._gpsd = gps3.GPSDSocket()
        self._data_stream = gps3.DataStream()

        self._gpsd.connect(host=self._host, port=self._port)
        self._gpsd.watch()


        self.solar_elevation = self.solar_azimuth = 0

        track_utc_time_change(hass, self.timer_update, second=30)

    @property
    def name(self):
        """Return the name."""
        return "GPS"

    @property
    def state(self):
        """Return the state of GPSD."""
        return "Here we are..."

    @property
    def state_attributes(self):
        """Return the state attributes of GPS."""
        return {
            ATTR_LATITUDE: 11111,
            ATTR_LONGITUDE: 2222,
            ATTR_ELEVATION: 33333,
            ATTR_GPS_TIME: 44444,
            ATTR_SPEED: 55555,
            ATTR_CLIMB: 66666,
            ATTR_FIX: 77777,
        }

    @property
    def next_change(self):
        """Datetime when the next change to the state is."""
        return min(self.next_rising, self.next_setting)

    def update_as_of(self, utc_point_in_time):
        """Calculate sun state at a point in UTC time."""
        print("#### GPS data: update as of....")


    def update_sun_position(self, utc_point_in_time):
        """Calculate the position of the sun."""
        print("#### GPS data: update as of....")


    def point_in_time_listener(self, now):
        """Called when the state of the sun has changed."""
        self.update_as_of(now)
        self.update_ha_state()

        # Schedule next update at next_change+1 second so sun state has changed
        track_point_in_utc_time(
            self.hass, self.point_in_time_listener,
            self.next_change + timedelta(seconds=1))

    def timer_update(self, time):
        """Needed to update solar elevation and azimuth."""
        self.update_sun_position(time)
        self.update_ha_state()
