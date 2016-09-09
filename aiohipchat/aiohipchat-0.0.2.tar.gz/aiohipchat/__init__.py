from functools import wraps

from aiohttp import web


class HipChatBot:
    def __init__(self, app, name, vendor_name, vendor_url, scopes, *,
                 description='', key=None, homepage='', bot_name=None,
                 allow_global=False, allow_room=True):
        self.initialized = False
        self._webhooks = []

        self._capabilities = {
            'name': name,
            'description': description,
            'key': key or name.replace(' ', '-').lower(),
            'links': {
                'homepage': homepage,
                'self': None,
            },
            'vendor': {
                'name': vendor_name,
                'url': vendor_url,
            },
            'capabilities': {
                'webhook': [],
                'hipchatApiConsumer': {
                    'fromName': bot_name or name,
                    'scopes': scopes,
                },
            },
            'installable': {
                'allowGlobal': allow_global,
                'allowRoom': allow_room,
                'callbackUrl': '/installed',
            }
        }

        self.app = app
        self.app.router.add_route('POST', '/installed', self._installed)
        self.app.router.add_route('GET', '/capabilities.json',
                                  self._capability_handler)

    def capabilities(self, host):
        """Lazily generate the capabilities that this bot can
        handle."""
        if not self.initialized:
            self._capabilities['links']['self'] = host
            self._capabilities['installable']['callbackUrl'] = \
                host + self._capabilities['installable']['callbackUrl']

            for hook in self._webhooks:
                hook['url'] = host + hook['url']
                self._capabilities['capabilities']['webhook'].append(hook)
            self.initialized = True
        return self._capabilities

    def resolve_host(self, request):
        return '{}://{}'.format(request.scheme, request.host)

    async def _capability_handler(self, request):
        """Create the capabilities payload for the install to hipchat"""
        return web.json_response(self.capabilities(self.resolve_host(request)))

    async def _installed(self, request):
        """Handled the installed callback event"""
        # TODO: Have strategy to cache tokens, use for verification
        # on webhooks
        return web.json_response({})

    def webhook(self, path, pattern=None, event='room_message', name=None):
        """
        Define a webhook handler, the wrapped method will be registered
        in as a webhook in the capabilities.
        :param path: relative path for the handler to listen on
        :param pattern: Optional pattern, this is the slash command. If not
                        provided the path will be used
        :param event: Event type that the hook should respond to
        :param name: capability name
        """
        pattern = pattern or '^' + path
        name = name or path

        self._webhooks.append({
            'url': path,  # host will be replaced during the request
            'pattern': pattern,
            'event': event,
            'authentication': 'jwt',  # TODO: validate, or allow ignore
            'name': name,
        })

        def _webhook(f):
            self.app.router.add_route('POST', path, f)

            @wraps(f)
            async def wrapper(*args, **kwargs):
                return await f(*args, **kwargs)
            return wrapper
        return _webhook


if __name__ == '__main__':
    # Simple example
    app = web.Application()

    hipchat = HipChatBot(app, 'deploymon', 'Matt Rasband', 'http://rasband.io',
                         ['view_messages'])

    @hipchat.webhook('/info')
    async def handle_info(request):
        return web.json_response({'message': 'Foo Bar'})

    web.run_app(app, port='8080')

