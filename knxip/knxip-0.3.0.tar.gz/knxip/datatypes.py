"""KNX data types

This implements some KNX data types and conversion methods
"""

from enum import Enum

class HVACMode(Enum):
    auto = 0
    comfort = 1
    standby = 2
    economy = 3
    building_protection = 4
    
    
    
