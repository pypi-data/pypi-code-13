"""
Cover platform that has a fake rollershutter, fake blinds, and a fake garage
door.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/demo/
"""
from homeassistant.components.cover import CoverDevice
from homeassistant.const import (STATE_CLOSED, STATE_OPEN, EVENT_TIME_CHANGED)
from homeassistant.helpers.event import track_utc_time_change


# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Setup demo cover platform."""
    add_devices_callback([
        DemoCover(hass, 'Rollershutter Kitchen', 100, False, False),
        DemoCover(hass, 'Blinds Bedroom', 60, True, True),
        DemoCover(hass, 'Garage Door', 0, True, False)
    ])


class DemoCover(CoverDevice):
    """Provides a demo cover."""

    # pylint: disable=no-self-use
    def __init__(self, hass, name, position, stop, tilt):
        """Initialize the roller shutter."""
        self.hass = hass
        self._name = name
        self._position = position
        self._stop = stop
        self._tilt = tilt
        self._opening = True
        self._listener = None

    @property
    def name(self):
        """Return the name of the demo cover."""
        return self._name

    @property
    def should_poll(self):
        """No polling needed for a demo cover."""
        return False

    @property
    def is_closed(self):
        """Return true if cover is closed."""
        return True if self._position == 0 else False

    @property
    def is_open(self):
        """Return true if cover is open."""
        return True if self._position > 0 else False

    @property
    def current_position(self):
        """Return the current position of the cover."""
        return self._position

    @property
    def can_stop(self):
        """Return true if cover is able to stop."""
        return self._stop

    @property
    def current_tilt(self):
        """Return the current tilt of the cover."""
        return STATE_CLOSED if self.can_tilt else STATE_OPEN

    def close_cover(self, **kwargs):
        """Close the cover."""
        if self._position == 0:
            return

        self._listen()
        self._opening = True

    def open_cover(self, **kwargs):
        """Open the cover."""
        if self._position == 100:
            return

        self._listen()
        self._opening = False

    def stop(self, **kwargs):
        """Stop the cover."""
        if self._listener is not None:
            self.hass.bus.remove_listener(EVENT_TIME_CHANGED, self._listener)
            self._listener = None

    @property
    def can_tilt(self):
        """Return true if cover is able to tilt."""
        return self._tilt

    def tilt_up_cover(self, **kwargs):
        """Tilt up the cover."""
        if self._position == 0:
            return

        self._listen()
        self._opening = True

    def tilt_down_cover(self, **kwargs):
        """TIlt down the cover."""
        if self._position == 100:
            return

        self._listen()
        self._opening = False

    def tilt_stop(self, **kwargs):
        """Stop the tilt of the cover."""
        if self._listener is not None:
            self.hass.bus.remove_listener(EVENT_TIME_CHANGED, self._listener)
            self._listener = None
    
    def _listen(self):
        """Listen for changes."""
        if self._listener is None:
            self._listener = track_utc_time_change(self.hass,
                                                   self._time_changed)

    def _time_changed(self, now):
        """Track time changes."""
        if self._opening:
            self._position -= 10
        else:
            self._position += 10

        if self._position % 100 == 0:
            self.stop()

        self.update_ha_state()