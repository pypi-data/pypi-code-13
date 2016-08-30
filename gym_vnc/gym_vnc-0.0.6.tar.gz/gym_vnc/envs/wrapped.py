from gym_vnc.envs import vnc_env, vnc_core_env

def WrappedVNCEnv(*args, **kwargs):
    return Unvectorize(Logger(vnc_env.VNCEnv(*args, **kwargs)))

def WrappedVNCCoreEnv(*args, **kwargs):
    return Unvectorize(Logger(vnc_core_env.VNCCoreEnv(*args, **kwargs)))

def WrappedVNCCoreSyncEnv(*args, **kwargs):
    return Unvectorize(Logger(vnc_core_env.VNCCoreSyncEnv(*args, **kwargs)))
