import importlib
import logging

def wrap(callee, logger, level=logging.INFO):
    try:
        (pkgname, callname) = callee.rsplit('.', 1)
        pkg = importlib.import_module(pkgname)
        func = getattr(pkg, callname)
    except Exception:
        logger.error('Could not wrap {}'.format(callee), exc_info=True)
        return

    child_logger = logger.getChild(callee)
    child_logger.setLevel(logging.NOTSET)

    def wrapper(*args, **kwargs):
        strargs = ', '.join(args)
        strkwargs = ', '.join(['{}={}'.format(k,kwargs[k]) for k in kwargs])
        child_logger.log(level, '--> ({}, {})'.format(strargs, strkwargs))
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            child_logger.log(level, '!!! {}'.format(e))
            raise
        child_logger.log(level, '<-- {}'.format(result))
        return result

    setattr(pkg, callname, wrapper)
