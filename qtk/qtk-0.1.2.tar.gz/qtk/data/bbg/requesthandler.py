import blpapi

from .defs import _bbglogger


def request_error_handler(e):
    _bbglogger.exception(e)


class BlpapiRequestHandler(object):

    def __init__(self, host="localhost", port=8194):
        self.options = blpapi.SessionOptions()
        self.options.setServerHost(host)
        self.options.setServerPort(port)
        self.session = None
        self.ref_data_service = None

    def __enter__(self):
        return self.start_session()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_session()

    def start_session(self):
        self.session = blpapi.Session(self.options)
        self.session.start()
        if not self.session.openService("//blp/refdata"):
            raise RuntimeError("Failed to open //blp/refdata")
        self.ref_data_service = self.session.getService("//blp/refdata")
        return self.session

    def stop_session(self):
        self.session.stop()

    def send_request(self, request_handler, event_handler,
                     error_handler=request_error_handler, output=None):
        """

        :param output: output `dict` to use if provided
        :param request_handler: function that fills out the bloomberg request
        :param event_handler: function that handles events
        :param error_handler: function that handles error
        :return:
        """
        request = request_handler(self.session)
        self.session.sendRequest(request)
        output = output if output is not None else {}
        try:
            while True:
                event = self.session.nextEvent(500)
                event_handler(event, output)

                if event.eventType() == blpapi.Event.RESPONSE:
                    break
        except Exception as e:
            error_handler(e)
        return output
