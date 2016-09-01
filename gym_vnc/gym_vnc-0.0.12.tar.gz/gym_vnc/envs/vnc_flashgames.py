from gym_vnc import spaces
from gym_vnc.envs import vnc_env

class VNCFlashgamesEnv(vnc_env.VNCEnv):
    pass

def mario_action(up=False, down=False, left=False, right=False, space=False):
    return [spaces.PointerEvent(10, 10),
            spaces.KeyEvent.by_name('up', down=up),
            spaces.KeyEvent.by_name('left', down=left),
            spaces.KeyEvent.by_name('right', down=right),
            spaces.KeyEvent.by_name('down', down=down),
            spaces.KeyEvent.by_name('space', down=down),
    ]
class VNCSuperMarioEnv(VNCFlashgamesEnv):
    safe_action_space = spaces.Hardcoded([
        mario_action(up=True),
        mario_action(up=True, left=True),
        mario_action(up=True, right=True),

        mario_action(down=True),
        mario_action(down=True, left=True),
        mario_action(down=True, right=True),

        mario_action(left=True),
        mario_action(right=True),

        mario_action(space=True),
    ])

def android_crash_action(up=False, left=False, right=False):
    return [spaces.PointerEvent(10, 10),
            spaces.KeyEvent.by_name('up', down=up),
            spaces.KeyEvent.by_name('left', down=left),
            spaces.KeyEvent.by_name('right', down=right),
    ]
class VNCAsteroidCrashEnv(VNCFlashgamesEnv):
    safe_action_space = spaces.Hardcoded([
        android_crash_action(up=True),
        android_crash_action(left=True),
        android_crash_action(right=True),
    ])
