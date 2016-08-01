import unisquid
import urllib
import wsgiref


class TestLiveServer(unisquid.LiveServerTestCase):
    def create_app(self):
        return wsgiref.simple_server.demo_app

    def test_server_process_is_spawned(self):
        thread = self.server_thread

        self.assertNotEqual(thread, None)
        self.assertTrue(thread.is_alive())

    def test_server_process_listening(self):
        response = urllib.urlopen(self.live_server_url)
        self.assertTrue(b'Hello world!' in response.read())
        self.assertEqual(response.code, 200)
