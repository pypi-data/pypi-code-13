"""
Copyright (c) 2016 Fabian Affolter <fabian@affolter-engineering.ch>

Licensed under MIT. All rights reserved.
"""
import unittest


class MyStromConnectionTest(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()

    def test_connect_tcp(self):
        @asyncio.coroutine
        def test_coro():
            try:
                client = MQTTClient()
                ret = yield from client.connect('mqtt://test.mosquitto.org/')
                self.assertIsNotNone(client.session)
                yield from client.disconnect()
                future.set_result(True)
            except Exception as ae:
                future.set_exception(ae)

        future = asyncio.Future(loop=self.loop)
        self.loop.run_until_complete(test_coro())
        if future.exception():
            raise future.exception()
