from awordaday.generators import FileBaseQuoteGenerator
from django.conf import settings


class TimezoneMiddleware(object):
    def __init__(self):
        self.word_generator = FileBaseQuoteGenerator(
            settings.AWORDADAY_WORDS_FILE)

    def process_response(self, request, response):
        response[
            getattr(settings, 'AWORDADAY_HEADER', 'X-A-Word-A-Day')] = next(
            self.word_generator)

        return response
