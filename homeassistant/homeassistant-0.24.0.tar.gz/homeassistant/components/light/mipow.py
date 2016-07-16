"""
Support for mipow lights.
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/light.mipow/
"""

import logging
import pygatt


from homeassistant.components.light import (
    ATTR_BRIGHTNESS, ATTR_RGB_COLOR, Light)

_LOGGER = logging.getLogger(__name__)

###REQUIREMENTS = ['pygatt==2.0.1']


# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Add device specified by serial number."""
    serial = config['serial']
    name = config.get('name')
    bulb = Mipow(serial, name)

    add_devices_callback([bulb])


class Mipow(Light):
    """Representation of a mipow light."""

    def __init__(self, serial, name=None):
        """Initialize the light."""
        if name is not None:
            self._name = name
        else:
            self._name = serial

        self._serial = serial
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
        if self._adapter is not None:
            self._stop_adapter()

        adapter = pygatt.backends.GATTToolBackend()
        adapter.start()

        self._adapter = adapter

        return adapter

    def _stop_adapter(self):
        self._adapter.stop()

    @property
    def should_poll(self):
        """Polling needed."""
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

        device_status = connection.char_read(
            "0000fffc-0000-1000-8000-00805f9b34fb")

        # Convert byte array into int list
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
        connection = adapter.connect(self._serial)

        if ATTR_RGB_COLOR in kwargs:
            self._rgb_color = [x for x in kwargs[ATTR_RGB_COLOR]]
            brgb = [0]
            brgb.append(self._rgb_color[0])
            brgb.append(self._rgb_color[1])
            brgb.append(self._rgb_color[2])

            connection.char_write_handle(0x0025, brgb)
        elif ATTR_BRIGHTNESS in kwargs:
            brgb = [kwargs[ATTR_BRIGHTNESS], 0, 0, 0]

            self._rgb_color = [255, 255, 255]
            connection.char_write_handle(0x0025, brgb)
        else:
            connection.char_write_handle(0x0025, [255, 0, 0, 0])
        connection.disconnect()

    def turn_off(self, **kwargs):
        """Turn the device off."""
        adapter = self._start_adapter()
        connection = adapter.connect(self._serial)
        connection.char_write_handle(0x0025, [00, 00, 00, 00])

        connection.disconnect()
        self._stop_adapter()