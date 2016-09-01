from gym_vnc.envs import vnc_env, vnc_core_env
from gym_vnc.wrappers.atari_wrappers import DiscreteToVNCAction, CropAtari, Throttle
from gym_vnc.wrappers.logger import Logger
from gym_vnc.wrappers.render import Render
from gym_vnc.wrappers.unvectorize import Unvectorize

def wrap(env):
    return Unvectorize(Render(Logger(env)))

def WrappedVNCEnv(*args, **kwargs):
    return wrap(vnc_env.VNCEnv(*args, **kwargs))

def WrappedVNCCoreEnv(*args, **kwargs):
    return wrap(vnc_core_env.VNCCoreEnv(*args, **kwargs))

def WrappedVNCCoreSyncEnv(*args, **kwargs):
    return wrap(vnc_core_env.VNCCoreSyncEnv(*args, **kwargs))

def WrappedVNCStarCraftEnv(*args, **kwargs):
    return wrap(vnc_env.VNCEnv(*args, **kwargs))

def WrappedVNCGTAVEnv(*args, **kwargs):
    return wrap(vnc_env.VNCEnv(*args, **kwargs))
