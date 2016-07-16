"""
Support for values stored in a file on a remote location.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.file/
"""
import logging
from datetime import timedelta

import voluptuous as vol
import requests

from homeassistant.const import (CONF_PLATFORM, CONF_NAME, STATE_UNKNOWN,
                                 CONF_VALUE_TEMPLATE)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers import template
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = 'File'
CONF_RESOURCE = 'resource'
CONF_UNIT_OF_MEASUREMENT = 'unit_of_measurement'
ICON = 'mdi:file-chart'

PLATFORM_SCHEMA = vol.Schema({
    vol.Required(CONF_PLATFORM): 'file',
    vol.Optional(CONF_NAME): cv.string,
    vol.Required(CONF_RESOURCE): cv.string,
    vol.Optional(CONF_UNIT_OF_MEASUREMENT): cv.string,
    vol.Optional(CONF_VALUE_TEMPLATE): cv.string,
})

# Return cached results if last scan was less then this time ago.
MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=60)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the file sensor."""
    resource = config.get(CONF_RESOURCE)
    name = config.get(CONF_NAME, DEFAULT_NAME)

    try:
        response = requests.get(resource, timeout=5)
        if not response.ok:
            _LOGGER.error('The given resource is not available: %s',
                          resource)
            return False
    except requests.exceptions.ConnectionError:
        _LOGGER.error('The URL is not accessible')
        return False

    data = FileData(resource)
    add_devices([FileSensor(name, data, config.get(CONF_UNIT_OF_MEASUREMENT),
                            config.get(CONF_VALUE_TEMPLATE))])


# pylint: disable=too-few-public-methods
class FileSensor(Entity):
    """Implementation of a file sensor."""

    def __init__(self, name, data, unit_of_measurement, value_template):
        """Initialize the sensor."""
        self.data = data
        self._name = name
        self._unit_of_measurement = unit_of_measurement
        self._value_template = value_template
        self.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit_of_measurement

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return ICON

    # pylint: disable=too-many-branches
    def update(self):
        """Get the latest data and update the states."""
        self.data.update()
        value = self.data.value
        print("#####  value", value)

        if value is None:
            value = STATE_UNKNOWN
        elif self._value_template is not None:
            value = template.render_with_possible_json_value(
                self._hass, self._value_template, value, STATE_UNKNOWN)

        self._state = value



# pylint: disable=too-few-public-methods
class FileData(object):
    """The class for handling the data retrieval."""

    def __init__(self, resource):
        """Initialize the data object."""
        self._resource = resource
        self.value = None

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest data from the remote system."""
        try:
            response = requests.get(self._resource, timeout=5)
            print("#####   response ", response.content)
            self.value = response.content
        except requests.exceptions.ConnectionError:
            _LOGGER.error('Unable to retrieve data')
            self.value = None
