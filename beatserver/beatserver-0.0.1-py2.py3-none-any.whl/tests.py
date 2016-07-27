import sys
import unittest
import argparse

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--port',
        type=int,
        help='Port number to listen on',
        default=8000,
    )
    parser.add_argument(
        '-b',
        '--bind',
        dest='host',
        help='The host/address to bind to',
        default="127.0.0.1",
    )
    return parser


class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = create_parser()


    def test_no_args(self):
        parsed = self.parser.parse_args()
        self.assertEqual(parsed.host, '127.0.0.1')
        self.assertEqual(parsed.port, 8000)

    def test_with_args(self):
        parsed = self.parser.parse_args(
            ['--bind', '127.0.0.1'], ['-p', '8000'])
        print parsed
        # self.assertEqual(parsed.p, 8000)
        self.assertEqual(parsed.host, '127.0.0.1')




if __name__ == '__main__':
    unittest.main()
