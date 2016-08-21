from functools import wraps
from .sns import SnsItem
from .s3 import S3Item


def s3(fn):
    @wraps(fn)
    def wrapper(event, context):
        item = S3Item(event, context)
        return fn(item)
    return wrapper


def sns(fn):
    @wraps(fn)
    def wrapper(event, context):
        item = SnsItem(event, context)
        return fn(item)
    return wrapper
