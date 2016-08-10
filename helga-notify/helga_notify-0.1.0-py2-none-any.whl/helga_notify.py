from helga import log
from helga.plugins.webhooks import authenticated, route


logger = log.getLogger(__name__)


@route('/notify/(?P<nick>[\w\-_]+)', methods=['POST'])
@authenticated
def notify(request, irc_client, nick):
    """
    An endpoint for sending a message to a nick. POST only. Must
    provide a single data param 'message'.
    """
    if nick.startswith('#'):
        request.setResponseCode(400)
        return 'To send a message to a channel, use the /announce route instead'

    message = request.args.get('message', [''])[0]
    if not message:
        request.setResponseCode(400)
        return 'Param message is required'

    logger.info('Sending message to %s: "%s"', nick, message)
    irc_client.msg(nick, message)

    return 'Message Sent'
