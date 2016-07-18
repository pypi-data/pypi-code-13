from unittest.mock import MagicMock

from tornado.concurrent import Future
from tornado.testing import AsyncTestCase

from messenger_sdk.container import BaseContainer
from messenger_sdk.fb_input import FbInput
from tests.sample_response import SampleTemplateResponse


class MessengerAsyncTestCase(AsyncTestCase):
    def setUp(self):
        super().setUp()
        self._fb_input = FbInput()
        self._event_factory = BaseContainer.event_factory()
        self._sample_template_response = SampleTemplateResponse()

    @staticmethod
    def get_async_function_mock(return_value):
        future = Future()
        future.set_result(return_value)
        return MagicMock(return_value=future)
