# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

# from subprocess import check_output, CalledProcessError
from pyvirtualdisplay import Display
from pyvirtualdisplay.xvnc import XvncDisplay, PROGRAM


class MyXvncDisplay(XvncDisplay):
    '''
    Xvnc wrapper
    '''
    @property
    def _cmd(self):
        cmd = [PROGRAM,
               '-depth', str(self.color_depth),
               '-geometry', '%dx%d' % (self.size[0], self.size[1]),
               '-rfbport', str(self.rfbport),
               # '-localhost',
               self.new_display_var,
               ]
        return cmd


class VNC(Display):
    '''
    Common class

    :param color_depth: [8, 16, 24, 32]
    :param size: screen size (width,height)
    :param bgcolor: background color ['black' or 'white']
    :param backend: 'xvfb', 'xvnc' or 'xephyr', ignores ``visible``
    '''

    @property
    def display_class(self):
        assert self.backend
        if self.backend == 'myxvnc':
            cls = MyXvncDisplay
        # TODO: check only once
        cls.check_installed()
        return cls

# #with VNC(backend='myxvnc',
# #             size=(900, 900),
# #             rfbport=str(5900),
# #             ) as disp:
# #    try:
# #        print('cmd', disp._cmd)
# #        print('opening')
# #        check_output(['firefox', '--new-instance', '-P', 'newx'])
# #    except CalledProcessError:
# #        raise
# #    except Exception, e:
# #        print(traceback.format_exc())
# #        print('Exception', e)
# #        retval = -1
# #        getstatusoutput(['xmessage', 'click to quit'], 30)
