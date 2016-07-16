"""
Support for XMPP message handling.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/mqtt/
"""
import logging
import os
import socket
import time
import sleekxmpp

import voluptuous as vol

from homeassistant.bootstrap import prepare_setup_platform
from homeassistant.config import load_yaml_config_file
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import template
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP,
    CONF_PLATFORM, CONF_SCAN_INTERVAL, CONF_VALUE_TEMPLATE, CONF_PASSWORD)

_LOGGER = logging.getLogger(__name__)

DOMAIN = "xmpp"

CONF_JABBER_ID = 'jid'
CONF_PROTOCOL = 'protocol'
CONF_TLS = 'tls'

DEFAULT_TLS = True


def setup(hass, config):
    """Start the MQTT protocol service."""
    conf = config.get(DOMAIN, {})

    jid = conf.get(CONF_JABBER_ID)
    password = conf.get(CONF_PASSWORD)
    use_tls = conf.get(CONF_TLS, DEFAULT_TLS)

    #global MQTT_CLIENT
    #try:
    XMPP_CLIENT = ControlBot(jid, password, use_tls)
    #except socket.error:
       # _LOGGER.exception("Can't connect to the broker. "
        #                  "Please check your settings and the broker "
       #                   "itself.")
       # return False

    return True

class ControlBot(sleekxmpp.ClientXMPP):
    """Service for sending Jabber (XMPP) messages."""

    # def __init__(self, ):
    #     """Initialize the Jabber Bot."""
    #     super(ControlBot, self).__init__(jid, password, use_tls)

    def __init__(self, jid, password, use_tls):
        """Initialize the control bot."""

        logging.basicConfig(level=logging.ERROR)

        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.use_tls = use_tls
        self.use_ipv6 = False
        self.add_event_handler('failed_auth', self.check_credentials)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

        self.connect(use_tls=self.use_tls, use_ssl=False)
        self.process()

    def start(self, event):
        """Start the communication and sends the message."""
        self.send_presence()
        self.get_roster()
        self.disconnect(wait=True)

    def check_credentials(self, event):
        """"Disconnect from the server if credentials are invalid."""
        self.disconnect()

    def message(self, msg):
        """Process incoming message stanzas."""
        if msg['type'] in ('chat', 'normal'):
            print("####", msg)
            msg.reply("Thanks for sending\n%(body)s" % msg).send()
