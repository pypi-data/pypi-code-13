import logging

from tornado import gen
from messenger_sdk.fb_response import FbResponse
from messenger_sdk.templates import Response
from messenger_sdk.fb_manager import FbManager
from messenger_sdk.events import EventFactory

from messenger_sdk.middlewares.middleware import Middleware, EventMiddleware, ResponseMiddleware


class MiddlewareListError(Exception):
    pass


class BaseHandler:
    _custom_middlewares = list()

    def __init__(self, event_factory: EventFactory, fb_manager: FbManager, base_middlewares: list):
        self._event_factory = event_factory
        self._fb_manager = fb_manager
        self._base_middlewares = base_middlewares

    @gen.coroutine
    def handle_entries(self, entries):
        for event in entries:
            try:
                logging.info('Input event: %s', event)
                event = self._event_factory.create_event(event)
                response = FbResponse()
                middleware_classes = self.load_middleware_classes()
                middleware_classes_count = len(middleware_classes)
                for index, middleware_class in enumerate(middleware_classes):
                    yield self._process_middleware(event=event,
                                                   response=response,
                                                   middleware_class=middleware_class)
                    if not event.propagate:
                        break
                    if response.send or index - 1 == middleware_classes_count:
                        yield self._fb_manager.send(response)
                        response = FbResponse()
            except Exception as err:
                logging.error('Unable to handle event: %s', err)
                response = Response(recipient_id=event.recipient_id,
                                    sender_action=Response.SENDER_ACTION_TYPING_OFF).__dict__()
                yield self._fb_manager.send(response)

    @staticmethod
    def _check_middleware_classes_list(middleware_classes):
        if middleware_classes is None:
            raise MiddlewareListError('Middleware classes list cannot be None.')
        if not isinstance(middleware_classes, list):
            raise MiddlewareListError('Middleware classes must be type of list')
        if len(middleware_classes) == 0:
            logging.warning('Empty middleware classes list.')

    def load_middleware_classes(self):
        base_middlewares = self._base_middlewares
        self._check_middleware_classes_list(base_middlewares)

        custom_middlewares = self._custom_middlewares
        self._check_middleware_classes_list(custom_middlewares)

        middlewares = base_middlewares + custom_middlewares

        return sorted(middlewares, key=lambda k: k['priority'], reverse=True)

    def _check_mw_type(self, mw_instance):
        if not isinstance(mw_instance, Middleware):
            raise TypeError('Expected {expected} class, {given} given in {self_name}.'.format(
                expected=Middleware.__class__.__name__,
                given=type(mw_instance).__name__,
                self_name=self.__class__.__name__))

    @gen.coroutine
    def _process_middleware(self, event, response, middleware_class):
        mw_instance = middleware_class.get('class')()
        self._check_mw_type(mw_instance)
        if not any(isinstance(event, supported_event) for supported_event in mw_instance.supported_events):
            return
        logging.debug('<--- Middleware: {middleware_name} --->'.format(middleware_name=mw_instance.__class__.__name__))
        if isinstance(mw_instance, EventMiddleware):
            logging.debug('Executing: {function_name}()'.format(function_name=mw_instance.process_event.__name__))
            yield mw_instance.process_event(event=event)
        if isinstance(mw_instance, ResponseMiddleware):
            logging.debug('Executing: {function_name}()'.format(function_name=mw_instance.process_response.__name__))
            yield mw_instance.process_response(event=event, response=response)
