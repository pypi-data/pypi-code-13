"""
Support for MiPow PlayBulbs.
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/light.playbulb/

Details: https://github.com/fabaff/Playbulb/blob/master/protocols/color.md
"""
import logging

import voluptuous as vol


from homeassistant.components.light import (ATTR_BRIGHTNESS, ATTR_RGB_COLOR,
                                            Light)
from homeassistant.const import (CONF_PLATFORM, CONF_NAME, STATE_UNKNOWN)
import homeassistant.helpers.config_validation as cv

###REQUIREMENTS = ['pygatt==2.0.1']

DEFAULT_NAME = 'PlayBulb'
CONF_MAC = 'mac'


PLATFORM_SCHEMA = vol.Schema({
    vol.Required(CONF_PLATFORM): 'playbulb',
    vol.Optional(CONF_NAME): cv.string,
    vol.Required(CONF_MAC): cv.string,
})

_LOGGER = logging.getLogger(__name__)


# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup of a MiPow PlayBulb Color."""
    mac = config.get(CONF_MAC)
    name = config.get(CONF_NAME, DEFAULT_NAME)

    add_devices([PlayBulpColor(mac, name)])


class PlayBulpColor(Light):
    """Representation of a PlayBulb."""

    def __init__(self, mac, name):
        """Initialize the light."""

        self._name = name
        self._mac = mac
        self._adapter = None

        try:
            self.update()
        except:
            self._rgb_color = [0, 0, 0]
            self._rgb_bright = [0, 0, 0, 0]

    def update(self):
        """Read back the device state."""
        self._rgb_color = self.rgb_color
        self._rgb_bright = self.rgb_bright

    def _start_adapter(self):
        """Start the adapter."""
        import pygatt

        if self._adapter is not None:
            self._stop_adapter()

        adapter = pygatt.backends.GATTToolBackend()
        adapter.start()

        self._adapter = adapter

        return adapter

    def _stop_adapter(self):
        """"Stop the adapter."""
        self._adapter.stop()

    @property
    def should_poll(self):
        """No Polling needed."""
        return False

    @property
    def name(self):
        """Return the name of the light."""
        return self._name

    @property
    def rgb_color(self):
        # Get device status from gattools
        adapter = self._start_adapter()
        connection = adapter.connect(self._serial)

        device_status = connection.char_read("0000fffc-0000-1000-8000-00805f9b34fb")

        #Convert byte array into int list
        device_colors = [x for x in device_status]

        # Remove first element as it's the brightness
        device_colors.pop(0)

        # Assign to instance for later use
        self._rgb_color = device_colors

        # Disconnect
        connection.disconnect()

        # Return list for ha use
        return self._rgb_color

    @property
    def rgb_bright(self):
        # Get device status from gattools
        adapter = self._start_adapter()
        connection = adapter.connect(self._serial)

        device_status = connection.char_read(
            "0000fffc-0000-1000-8000-00805f9b34fb")

        # Convert byte array into int list
        device_bright = [x for x in device_status]

        # Remove first element as it's the brightness

        # Assign to instance for later use
        self._rgb_bright = device_bright

        # Disconnect
        connection.disconnect()

        # Return list for ha use
        return self._rgb_bright

    @property
    def is_on(self):
        """Check whether any of the LEDs colors are non-zero."""
        return sum(self._rgb_color) + sum(self._rgb_bright) > 0

    def turn_on(self, **kwargs):
        """Turn the device on."""
        adapter = self._start_adapter()
        connection = adapter.connect(self._mac)

        if ATTR_RGB_COLOR in kwargs:
            self._rgb_color = [x for x in kwargs[ATTR_RGB_COLOR]]
            brgb = [0]
            brgb.append(self._rgb_color[0])
            brgb.append(self._rgb_color[1])
            brgb.append(self._rgb_color[2])

            connection.char_write_handle(0x0018, brgb)
        elif ATTR_BRIGHTNESS in kwargs:
            brgb = [kwargs[ATTR_BRIGHTNESS], 0, 0, 0]

            self._rgb_color = [255, 255, 255]
            connection.char_write_handle(0x0018, brgb)
        else:
            connection.char_write_handle(0x0018, [255, 0, 0, 0])
        connection.disconnect()

    def turn_off(self, **kwargs):
        """Turn the device off."""
        adapter = self._start_adapter()
        connection = adapter.connect(self._mac)
        connection.char_write_handle(0x0016, [00, 00, 00, 00])

        connection.disconnect()
        self._stop_adapter()