__version__ = '1.0.14'


def background(*arg, **kw):
    from background_task.tasks import tasks
    return tasks.background(*arg, **kw)
