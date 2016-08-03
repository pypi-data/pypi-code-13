# coding: utf-8

import unittest

from twitprof.scrapper.scrapper import TwitterScrapper


class TwitterScrapperTestCase(unittest.TestCase):

    def test_get_user_data(self):
        scrapper = TwitterScrapper(consumer_key=u"vSBxMNSibpggfl3MJtsYInneZ",
                                   consumer_secret=u"cITyo6IT17jqoQQTOqMsvk6uJ3BrZhHi7i72OM8cBBU2960ld3",
                                   access_token=u"758731102253043712-Zy9QdaPi9x7pcUg4G7WTt4me8yILihv",
                                   access_token_secret=u"RYOnbq0hwBBXItkyGDgGN4GxmfiPKgm72A9XqFPUhFOJc")
        user = scrapper.get_user_data("20981247")
        self.assertEqual(user["popularity"], 0)
        self.assertEqual(user['name'], u"Phillip Meredith")


if __name__ == '__main__':
    unittest.main()
