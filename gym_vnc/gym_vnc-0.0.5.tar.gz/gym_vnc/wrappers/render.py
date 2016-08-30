import logging
import os
from twisted.python.runtime import platform

from gym_vnc.wrappers import vnc_wrapper

logger = logging.getLogger(__name__)

class Render(vnc_wrapper.VNCWrapper):
    def __init__(self, *args, **kwargs):
        if platform.isLinux() and not os.environ.get('DISPLAY'):
            self.renderable = False
        else:
            self.renderable = True
        super(Render, self).__init__(*args, **kwargs)

    def _render(self, *args, **kwargs):
        if not self.renderable:
            return
        # Could log, but no need
        return self.env.render(*args, **kwargs)
