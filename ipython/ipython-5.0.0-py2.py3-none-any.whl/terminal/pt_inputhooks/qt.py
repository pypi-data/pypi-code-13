import sys
from IPython.external.qt_for_kernel import QtCore, QtGui

def inputhook(context):
    app = QtCore.QCoreApplication.instance()
    if not app:
        return
    event_loop = QtCore.QEventLoop(app)

    if sys.platform == 'win32':
        # The QSocketNotifier method doesn't appear to work on Windows.
        # Use polling instead.
        timer = QtCore.QTimer()
        timer.timeout.connect(event_loop.quit)
        while not context.input_is_ready():
            timer.start(50)  # 50 ms
            event_loop.exec_()
            timer.stop()
    else:
        # On POSIX platforms, we can use a file descriptor to quit the event
        # loop when there is input ready to read.
        notifier = QtCore.QSocketNotifier(context.fileno(), QtCore.QSocketNotifier.Read)
        notifier.setEnabled(True)
        notifier.activated.connect(event_loop.exit)
        event_loop.exec_()
