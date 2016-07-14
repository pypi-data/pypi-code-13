#coding:utf-8
import os
import sys
import threading
import time
import datetime
import traceback
import inspect
import json

APP_NAME = None


def set_app_name(name):
    global APP_NAME
    APP_NAME = name


def installThreadExcepthook():
    init_old = threading.Thread.__init__

    def init(self, *args, **kwargs):
        init_old(self, *args, **kwargs)
        run_old = self.run

        def run_with_except_hook(*args, **kw):
            try:
                run_old(*args, **kw)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                sys.excepthook(*sys.exc_info())
        self.run = run_with_except_hook
    threading.Thread.__init__ = init


def log_exception(excType, excValue, tb, ):
    exc = traceback.format_exception(excType, excValue, tb)
    exc = ''.join(exc)

    frame = get_last_tb(tb).tb_frame
    file_name = frame.f_code.co_filename
    func_name = frame.f_code.co_name
    func_args = {}
    for key in inspect.getargvalues(frame).args:
        func_args[key] = str(inspect.getargvalues(frame).locals[key])

    data = {
        'func_name': func_name,  # 调用函数名
        'func_args': func_args,  # 函数调用
        'exception_name': excValue.__class__.__name__,  # 异常名称
        'exception_info': exc,  # 异常信息
        # 'ext_param': '', #自定义异常内容参数
        'timestamp': time.time(),  # 异常时间
    }

    global APP_NAME
    if not APP_NAME:
        APP_NAME = file_name
    f = open(get_log_file_name(), 'a')
    f.write(json.dumps(data) + '\n')
    f.flush()
    f.close()


def get_last_tb(tb):
    while tb.tb_next != None:
        tb = tb.tb_next
    return tb


def get_log_file_name():
    # 日志路径格式: $DSB_WARNING_LOG/{application_name}/YYYY/MM/DD_exception.log
    log_path = os.environ.get('DSB_WARNING_LOG')
    if log_path:
        if log_path.endswith('/'):
            log_path = log_path[:-1]
    else:
        log_path = '/var/log/vacuum'

    file_name = '{}/{}/{:%Y/%m/%d}_exception.log'.format(
        log_path, APP_NAME, datetime.datetime.now())

    path = file_name[:file_name.rfind('/')]
    if not os.path.exists(path):
        os.makedirs(path)

    return file_name


sys.excepthook = [log_exception, sys.__excepthook__][0]
installThreadExcepthook()

if __name__ == "__main__":
    # export DSB_WARNING_LOG=abc
    # export DSB_WARNING_LOG=
    env = 'DSB_WARNING_LOG'
    log_path = os.environ.get(env)
    if log_path:
        print(env, log_path)
    # quit()

    def foo(a, b, c):
        a = 1 / 0

    threading.Thread(target=foo, args=(1, 2, 9)).start()
    # foo()
