# coding: utf-8
import os
import unittest
from test.test_support import EnvironmentVarGuard


from twitprof import scraper

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class ScraperTestCase(unittest.TestCase):

    def test_load_scraper_from_config_file(self):
        scraper_config_filepath = os.path.join(CURRENT_DIR, 'config', 'scraperconfig.cfg')

        with EnvironmentVarGuard() as env:
            env.set('SCRAPER_CONFIG_TEST', scraper_config_filepath)
            loaded_scraper = scraper.load_scraper_from_envvar('SCRAPER_CONFIG_TEST')
        self.assertIsNotNone(loaded_scraper)
        self.assertIsInstance(loaded_scraper, scraper.TwitterScraper)

    def test_load_scraper_from_empty_config_file(self):
        scraper_config_filepath = os.path.join(CURRENT_DIR, 'config', 'scraperconfigempty.cfg')

        with EnvironmentVarGuard() as env:
            env.set('SCRAPER_CONFIG_TEST', scraper_config_filepath)
            with self.assertRaises(ValueError) as raises_context:
                scraper.load_scraper_from_envvar('SCRAPER_CONFIG_TEST')
        expected_message = "Scraper configuration not found in file {}".format(scraper_config_filepath)
        self.assertEqual(raises_context.exception.message, expected_message)

    def test_load_scraper_from_config_missing_envar(self):
        with self.assertRaises(ValueError) as raises_context:
            scraper.load_scraper_from_envvar('SCRAPER_CONFIG_TEST')
        self.assertEqual(raises_context.exception.message, "Environment variable SCRAPER_CONFIG_TEST not set")


if __name__ == '__main__':
    unittest.main()
