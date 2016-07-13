from peche.logging import Level
import logging

stp = {
    10: Level.Debug,
    20: Level.Info,
    30: Level.Warn,
    40: Level.Error,
    50: Level.Critical
}

pts = {
    Level.Debug: 10,
    Level.Info: 20,
    Level.Warn: 30,
    Level.Error: 40,
    Level.Critical: 50
}

from peche.logging.bridge.handler import BridgeHandler as Bridge
from peche.logging.bridge.bridge import bridge