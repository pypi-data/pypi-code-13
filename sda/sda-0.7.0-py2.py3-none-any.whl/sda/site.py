"""Site
"""

from shortcuts import encode_ascii
import re
from selenium.webdriver.remote.webdriver import WebDriver


__author__ = 'jlane'
__copyright__ = 'Copyright (c) 2016 FanThreeSixty'
__license__ = "MIT"
__version__ = '0.7.0'
__contact__ = 'jlane@fanthreesixty.com'
__status__ = 'Alpha'
__docformat__ = 'reStructuredText'

__all__ = ['Site']


class Site(object):
    """The Site Implementation

    The intention for the Site object is to contain all website pages. An example usage of this might be:

    Let's say we have the following file structure

    my_project
        - __init__.py
        - main.py
        - page_1
            - __init__.py
            - fixtures.py
            - locators.py
            - page.py
        - page_2
            - __init__.py
            - fixtures.py
            - locators.py
            - page.py

        - site
            - __init__.py
            - site.py
            - settings.py


    site/site.py

    .. code-block:: python

        from sda.site import Site
        from page_1.page import Page1
        from page_2.page import Page2

        class ExampleSite(Site):

            def __init__(self, web_driver):

                super(ExampleSite, self).__init__(web_driver)
                self.page_1 = Page1(web_driver)
                self.page_2 = Page2(web_driver)

    """

    RE_URL = r'^(?:(?P<protocol>[a-zA-Z]+):\/\/)?(?P<domain>[\w\d\.-]+\.[\w]{2,6})(?P<path>[\/\w\-\.\?]*)$'

    def __init__(self, web_driver):
        """Website element

        :param WebDriver web_driver: Selenium webdriver
        :return:
        :raises TypeError: If web_driver is not a Selenium WebDriver
        """

        # Instantiate WebDriver
        self.driver = web_driver if isinstance(web_driver, WebDriver) else None

        if not self.driver:
            raise TypeError("'web_driver' MUST be a selenium WebDriver element")

    @property
    def domain(self):
        """Returns the domain for a website
       
        :return: domain
        :rtype: str
        """

        results = re.match(self.RE_URL, self.url)

        if results:

            try:
                return results.group("domain")

            except IndexError:
                pass

        return ''

    @property
    def path(self):
        """Returns the website path

        :return: path
        :rtype: str
        """

        results = re.match(self.RE_URL, self.url)

        if results:

            try:
                return results.group("path")

            except IndexError:
                pass

        return ''

    @property
    @encode_ascii()
    def url(self):
        """Current page URL

        :return: Page URL
        :rtype: str
        """

        return self.driver.current_url
