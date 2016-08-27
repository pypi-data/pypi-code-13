from django.views import generic
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from djmessenger.receiving import Callback
from djmessenger.handling import BaseHandler
from djmessenger.sending import CommonSender


logger = logging.getLogger(__name__)


class DJMBotView(generic.View):
    def get(self, request, *args, **kwargs):
        verify_token = self.request.GET.get('hub.verify_token', None)
        challenge = self.request.GET.get('hub.challenge', None)
        if verify_token and challenge:
            return HttpResponse(challenge)
        else:
            logger.error('Either verify_token [%s] or challenge [%s] not found '
                         'in url parameter' % (verify_token, challenge))
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        from djmessenger.routing import policy

        body = self.request.body.decode('utf-8')
        incoming_message = json.loads(body)
        # logger.debug('DJM_HANDLERS: %s' % DJM_HANDLERS)
        try:
            callback = Callback.deserialize(incoming_message)
            assert isinstance(callback, Callback)
            # save user profile if settings to True
            for entry in callback.entry:
                for messaging in entry.messaging:
                    # UserProfileHandler(messaging).handle()
                    # for clazz in DJM_HANDLERS:
                    handlers = policy.get_handlers(messaging.get_receiving_type())
                    logger.debug('Ready to process messaging of ReceivingType %s' % messaging.get_receiving_type())
                    logger.debug('Got applicable routing handler classes from policy: %s' % handlers)
                    for handler in handlers:
                        if not issubclass(handler.get_class(), BaseHandler):
                            continue
                        logger.debug('Routing message %s to handler %s' % (messaging, handler))
                        handler_instance = handler.get_class()(messaging, *handler.get_args())
                        if handler_instance.should_handle():
                            handler_instance.handle()
                        senders = policy.get_senders(messaging.get_receiving_type(), handler)
                        logger.debug('Handler jobs are done, ready to send using senders: %s' % senders)
                        for sender in senders:
                            if not issubclass(sender.get_class(), CommonSender):
                                continue
                            logger.debug('Sending to user using sender %s' % sender)
                            sender_instance = sender.get_class()(messaging.get_psid(), *sender.get_args())
                            sender_instance.send()
        except Exception as e:
            logging.exception('Got exception on post...')
            logger.error('Failed to handle the message because %s' % e)
        return HttpResponse()
