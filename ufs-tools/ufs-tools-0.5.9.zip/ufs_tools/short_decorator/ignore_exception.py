import traceback


def ignore_exc(func):
    """
    Usage:
    @ignore_exc
    def test(a):
        pass
    :param func: the function we want to ignore exception
    :return:
    """
    return ignore_exc_with_result()(func)


def ignore_exc_with_result(exception_result=None, exception=Exception):
    """
    Usage:
    @ignore_exc_with_result()(func)
    def test(a):
        pass
    :param exception_result:
    :param exception:
    :return:
    """
    # Ref: http://wklken.me/posts/2012/10/27/python-base-decorator.html
    def exc_wrapper(func):
        # print "executing--------------"
        def wrap_with_exc(*args):
            # noinspection PyBroadException
            try:
                # print "executing!!!!!!!!!!!!!!!!"
                return func(*args)
            except exception, e:
                print "ignored the following exception:________________________________________________"
                traceback.print_exc()
                return exception_result

        return wrap_with_exc

    return exc_wrapper
