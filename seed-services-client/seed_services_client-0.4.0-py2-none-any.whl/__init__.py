"""Seed Services client library."""

from .identity_store import IdentityStoreApiClient
from .stage_based_messaging import StageBasedMessagingApiClient
from .auth import AuthApiClient
from .control_interface import ControlInterfaceApiClient
from .hub import HubApiClient
from .message_sender import MessageSenderApiClient

__version__ = "0.4.0"

__all__ = [
    'IdentityStoreApiClient', 'StageBasedMessagingApiClient', 'AuthApiClient',
    'ControlInterfaceApiClient', 'HubApiClient', 'MessageSenderApiClient'
]
