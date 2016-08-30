from .scrapper import scrapper
from .database import Database
from .basket import Basket
from .user import User
from .interface import Print

import time
import datetime
import logging
import os

WEBSITE = {'BE': ['https://www.pizza.be', ["/en", "/nl", "/fr", "/de"]],  # Ok
           'EN': ['https://www.takeaway.com', [""]],  # Not working (new website)
           'FR': ['https://www.pizza.fr', [""]],  # Ok
           'NL': ['https://www.thuisbezorgd.nl', [""]],  # Ok
           'AT': ['https://www.lieferservice.at', [""]],  # Ok
           'CH': ['https://www.lieferservice.ch', [""]],  # Ok
           'DK': ['https://www.pizza.dk', [""]],  # Not working postcode is not valid
           'LU': ['https://www.pizza.lu', [""]],  # Ok
           'PT': ['https://www.pizza.pt', [""]],  # Ok
           'DE': ['https://www.lieferservice.de/', [""]],  # Not working (website different)
           'DD': ['https://www.lieferando.de/#!', [""]],  # Not working (website different)
           'PL': ['https://pyszne.pl/', [""]],  # Not working (website different)
           'VT': ['https://www.vietnammm.com/en/', [""]]  # Not working (website different)
           }


class TakeAway:
    def __init__(self, country, postcode, interface=None):
        country = country.upper()
        logging.info("Init of TakeAway: {} {}".format(country, postcode))
        self.website = WEBSITE[country][0]
        self.language = WEBSITE[country][1][0]

        if interface is None:
            self.interface = Print(country, postcode)
        else:
            self.interface = interface

        self.scrapper = scrapper.get_scrapper(country, postcode)
        self.database = Database(country, postcode, self.scrapper, self.interface, os.path.dirname(__file__))  # Init database
        self.basket = Basket(self.website + self.language, self.database)  # Init basket
        self.user = User(self.database, self.interface)  # Init user

        self.obsolete_restaurant()

    def obsolete_restaurant(self):
        """
        Print the number of restaurant not updated since one month for the current postcode
        :return: None
        """
        date = datetime.date.today() - datetime.timedelta(days=30)
        old, _ = self.database.search(restaurant_searches=True, updated=date)
        logging.info("{} obsolete restaurant".format(len(old)))
        logging.debug(old)
        if old:
            self.interface.print(
                "Information about {} restaurants are more than a month old.\nRun --db-update to update the obsolete\
                restaurants or --db-make to update all the database.".format(
                    len(old)))

    def make_database(self, output=False):
        """
        Delete the old and make a new database for the postcode
        :param output: True to output information about the progress
        :return: True
        """
        # Scrap everything
        logging.info("Making database")
        if output:
            self.interface.print("Fetching data...")
        url = self.scrapper.get_postcode_url()
        data = self.scrapper.get_restaurants_name(url)
        return self.download_restaurants(data, output=output)

    def update_database(self, output=False, days=30):
        """
        Update the restaurant not updated for days
        :param output: True to output information about the progress
        :param days: Number of days since last update
        :return: True or False if no restaurant to update
        """
        logging.info("Updating database")
        if output:
            self.interface.print("Fetching data...")
        date = datetime.date.today() - datetime.timedelta(days=days)
        logging.debug(date)
        restaurants, _ = self.database.search(restaurant_searches=True, updated=date)
        if restaurants:
            logging.info("{} restaurants to update".format(len(restaurants)))
            data = dict()
            for restaurant in restaurants:
                logging.debug(restaurant)
                data[restaurant.name] = {"url": restaurant.url}
            return self.download_restaurants(data, output=output)
        else:
            logging.info("No restaurant to update")
            return False

    def consolidate_database(self, output=False):
        """
        Consolidate the database for the postcode. Download only restaurants not already in the database.
        :param output: True to output information about the progress
        :return: True
        """
        logging.info("Consolidating database")
        if output:
            self.interface.print("Fetching data...")

        url = self.scrapper.get_postcode_url()
        data = self.scrapper.get_restaurants_name(url)
        db_restaurants, _ = self.database.search(restaurant_searches=True)
        logging.debug(data)
        logging.debug(db_restaurants)
        for db_restaurant in db_restaurants:
            if [db_restaurant.name, db_restaurant.url] in data:
                data.remove([db_restaurant.name, db_restaurant.url])
        logging.info("{} restaurants to download".format(len(data)))
        if len(data) != 0:
            return self.download_restaurants(data, output=output)
        else:
            return False

    def download_restaurants(self, data, output=False):
        """
        Download and save the restaurants in data. If more than 30 restaurants download by step of 30 and wait.
        Should only be call by make/update/consolidate database
        :param data: list of restaurants to download
        :param output: True to output information about the progress
        :return: dict of restaurants data
        """
        restaurants = self.scrapper.get_restaurants_info(data, self.interface, output=output)
        time.sleep(0.2)
        self.interface.print("Saving to database...")
        time.sleep(0.2)
        return self.database.update_database(restaurants, self.interface)

    def checkout(self, remarks=True, confirm=False):
        """
        Checkout the basket and order your meal
        :param remarks: Remarks to add to the order
        :param confirm: Confirm the checkout
        :return: list of items checked on the online basket
        """
        logging.info("Checkout, confirm: {}".format(confirm))
        if remarks is True:
            remarks = ''

        if not self.user.user:
            self.user.user = self.user.create_user()

        items_checked, restaurant_name = self.scrapper.checkout(self.basket.items, remarks=remarks,
                                                                user_info=self.user.user, confirm=confirm,
                                                                postcode=self.database.postcode)

        return confirm, items_checked, restaurant_name, self.basket.total, "{}, {}".format(self.user.user.address,
                                                                                           self.user.user.city)

    def teardown(self):
        """
        Teardown the database session use by this instance.
        To call before creating a new instance for changing the postcode
        :return: None
        """
        logging.debug(
            "Teardown of TakeAway: {} {}".format(self.database.postcode.country, self.database.postcode.postcode))
        self.database.session.close()


if __name__ == "__main__":
    pass
