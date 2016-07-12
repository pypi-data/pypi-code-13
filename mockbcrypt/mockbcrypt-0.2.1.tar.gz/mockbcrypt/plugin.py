import logging
import os
from mock import patch
from nose.plugins import Plugin

log = logging.getLogger('nose.plugins.mockbcrypt')


class MockBcryptPlugin(Plugin):
    name = 'mockbcrypt'

    def options(self, parser, env=os.environ):
        super(MockBcryptPlugin, self).options(parser, env=env)

    def configure(self, options, conf):

        super(MockBcryptPlugin, self).configure(options, conf)
        if not self.enabled:
            return
        encrypt_patcher = patch('passlib.hash.bcrypt.encrypt')
        encrypt = encrypt_patcher.start()
        encrypt.side_effect = lambda x: x

        verify_patcher = patch('passlib.hash.bcrypt.verify')
        verify = verify_patcher.start()
        verify.side_effect = lambda x, y: x == y

    def finalize(self, result):
        log.info('MockBcrypt pluginized world!')
