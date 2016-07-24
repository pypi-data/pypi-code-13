import os

import hark.context
import hark.log


class BuilderContext(hark.context.Context):
    """
    Extends the base hark context to have a directory for build artifacts.
    """

    def __init__(self, path):
        self.builder_path = os.path.join(path, 'builder')
        hark.context.Context.__init__(self, path)

    def _initialize(self, path):
        hark.context.Context._initialize(self, path)

        if not os.path.exists(self.builder_path):
            hark.log.info('Creating hark builder dir: %s', self.builder_path)
            os.mkdir(self.builder_path)
