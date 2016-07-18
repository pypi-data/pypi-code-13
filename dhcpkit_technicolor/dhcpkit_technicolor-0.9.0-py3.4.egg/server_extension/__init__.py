"""
Handlers for the options defined in dhcpkit_technicolor.options
"""
from dhcpkit.ipv6.server.handlers.basic import OverwriteOptionHandler

from dhcpkit_technicolor.options import SolMaxRTTechnicolorOption


class SolMaxRTTechnicolorOptionHandler(OverwriteOptionHandler):
    """
    Handler for putting SolMaxRTTechnicolorOption in responses
    """

    def __init__(self, sol_max_rt: int, always_send: bool = False):
        option = SolMaxRTTechnicolorOption(sol_max_rt=sol_max_rt)
        option.validate()

        super().__init__(option, always_send=always_send)

    def __str__(self):
        return "{} with {}".format(self.__class__.__name__, self.option.sol_max_rt)
