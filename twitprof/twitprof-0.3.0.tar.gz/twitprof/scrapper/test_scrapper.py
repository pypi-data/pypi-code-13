# coding: utf-8

import unittest

from twitprof.scrapper.scrapper import get_user_data


class TwitterScrapperTestCase(unittest.TestCase):

    def test_get_user_data(self):
        user = get_user_data("santiavenda2")
        print user
        self.assertEqual(user["popularity"], 27)
        self.assertEqual(user['name'], u"Santiago Avendaño")


if __name__ == '__main__':
    unittest.main()
