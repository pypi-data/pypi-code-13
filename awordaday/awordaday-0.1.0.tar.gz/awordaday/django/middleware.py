from django.conf import settings


class QuoteMiddleware(object):
    def __init__(self):
        self.generators = getattr(settings, 'AWORDADAY_GENERATORS', {})

    def process_response(self, request, response):
        for header, generator in self.generators.items():
            response[header] = next(generator)
        return response
