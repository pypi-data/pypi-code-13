#!/usr/bin/env python

from takeaway.interface import Print
from takeaway.user.error import UserError
from takeaway.scrapper.error import ScrapperError
from takeaway.database.database import DatabaseError
from takeaway.basket.basket import BasketError
from takeaway.main import TakeAway

from logging.handlers import RotatingFileHandler

import sys
import re
import logging
import argparse
import time
import os


def log(debug):
    logger_formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(filename)s:%(funcName)s - %(message)s')
    path = os.path.dirname(__file__)
    file_handler = RotatingFileHandler(os.path.join(path, "takeaway.log"),maxBytes=100000, backupCount=1)
    file_handler.setFormatter(logger_formatter)
    logger = logging.getLogger()
    logger.addHandler(file_handler)

    if debug is not False:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logger_formatter)
        logger.addHandler(console_handler)
        if type(debug) is int:
            logger.setLevel(debug)
        else:
            logger.setLevel(20)
    else:
        logger.setLevel(40)


def main():
    parser = argparse.ArgumentParser(description="Command line interface for pizza.be.")
    parser.add_argument('country', action="store", help="Your country (BE, EN, ...).", default=None,
                        metavar='country')
    parser.add_argument('postcode', action="store", help="""Your postcode (1000, "W1J 0", ...).""",
                        default=None, metavar='postcode')
    parser.add_argument('-i', action="store_true", default=False, dest="interactive",
                        help="Deactivate the interactive mode.")
    parser.add_argument('--checkout', action="store", default=False, const=True, dest="checkout", nargs="?",
                        help="Order your basket.", metavar="remarks", type=str)
    parser.add_argument('--confirm', action="store_true", default=False, dest="confirm",
                        help="Confirm the checkout.")
    parser.add_argument('--postcode', action="store", nargs=2, default=False, dest='new_postcode',
                        help="Use this to change current postcode.", metavar=('country', 'postcode'))
    parser.add_argument('--debug', action="store", default=False, const=True, nargs="?", dest="log_lvl",
                        metavar="level", help="Display debugging message and save to filename", type=int)

    group_search = parser.add_argument_group('Search')
    group_search.add_argument('-m', action="store", help="Search a meal (default is all).",
                              dest="search_meal", nargs='*', default=False, metavar='meal')
    group_search.add_argument('-c', action="store",
                              help="Search for a category(default is all).",
                              dest="search_cat", nargs='*', default=False, metavar="category")
    group_search.add_argument('-r', action="store",
                              help="Search for a restaurant (default is all).",
                              dest="search_rest", nargs='*', default=False, metavar="restaurant")
    group_search.add_argument('-v', action="count", default=1, dest='verbose',
                              help="Level of information to display. Use only with -r. 2 levels available.")
    group_search.add_argument('--time', action='store_true', default=False, dest="time",
                              help="Select only currently open restaurant")

    group_db = parser.add_argument_group('Database')
    group_db_me = group_db.add_mutually_exclusive_group()
    group_db_me.add_argument('--db-list', action="store", default=False, const="all", dest="db_list",
                             help='List all postcodes in the database.', nargs="?", metavar="country")
    group_db_me.add_argument('--db-del', action="store", default=False, dest="db_del", nargs=2,
                             help="Delete the postcode from the database.", metavar=('country', 'postcode'))
    group_db_me.add_argument('--db-make', action='store_true', default=False, dest="db_make",
                             help="Make the database for this postcode.")
    group_db_me.add_argument('--db-update', action='store', nargs='?', default=False, const=True,
                             dest="db_update", type=int, help="Update the database for this postcode.",
                             metavar="days")
    group_db_me.add_argument('--db-consolidate', action='store_true', default=False,
                             dest="db_consolidate", help="Consolidate the database for this postcode.",)

    group_basket = parser.add_argument_group('Basket')
    group_basket.add_argument('-a', action="store", default=False, dest="ba_add", nargs="+", type=int,
                              help="Index of item(s) to add to basket.", metavar='index')
    group_basket.add_argument('-d', action="store", default=False, dest="ba_del", nargs="+", type=int,
                              help="Index of item(s) to delete from the basket.", metavar="index")
    group_basket.add_argument('-l', action="store_true", default=False, dest="ba_list",
                              help="List all the item(s) in the basket.")
    group_basket.add_argument('--clear-basket', action="store_true", default=False, dest="ba_clear",
                              help="Clear all the item(s) in the basket")

    group_user = parser.add_argument_group('User')
    group_user.add_argument('-u', action="store", default=False, dest='u_name', metavar="user", nargs="?",
                            const=True,
                            help="User to use for checkout.")
    group_user.add_argument('--u-create', action="store", default=False, dest="u_new", metavar="user",
                            help="Create or modify an user.")
    group_user.add_argument('--u-list', action="store_true", default=False, dest="u_list",
                            help="List the users in the database.")
    group_user.add_argument('--u-del', action="store", default=False, dest="u_del", metavar="user", nargs="?",
                            const=True, help="Delete the user.")

    args = parser.parse_args()  # argparse
    log(args.log_lvl)
    user_input = None
    interface = Print(args.country, args.postcode)  # Init the interface
    try:
        takeaway = TakeAway(args.country, args.postcode, interface)  # Init PizzaCli class
    except ScrapperError as e:  # If postcode not in database and no network access the init fail.
        logging.critical("Can not init PizzaCli: {} {}".format(args.country.upper(), args.postcode))
        interface.custom_error(e)
        sys.exit(0)
    ask_user_input = False  # Don't ask for user_input during the first loop

    while True:
        if ask_user_input:
            time.sleep(0.1)  # Waiting to avoid overlapping print
            user_input = get_input(takeaway, interface)  # Ask for user input
        ask_user_input = True  # After first loop we ask user input

        if user_input:  # If we have a clean input we try to parse it with argsparse
            try:
                args = parser.parse_args(user_input)
            except SystemExit:  # Catch SystemExist of argsparse and continue and re-ask user for input
                time.sleep(0.1)  # Wait to avoid overlapping print
                continue

        # Change postcode
        if args.new_postcode:
            if len(args.new_postcode) == 2:
                interface = Print(args.new_postcode[0], args.new_postcode[1])
                takeaway.teardown()  # Teardown the old TakeAway instance
                try:
                    takeaway = TakeAway(args.new_postcode[0], args.new_postcode[1], interface)  # Create new instance
                except ScrapperError as e:
                    interface.custom_error(e)
                    continue
            else:
                interface.print("Postcode must be in the format BE 1420!")

        # User call
        if args.u_name:
            try:
                interface.load_unload_user(takeaway.user.load_unload_user(args.u_name))
            except UserError as e:
                interface.custom_error(e)
        if args.u_del:
            try:
                interface.delete_user(takeaway.user.delete_user(args.u_del))
            except UserError as e:
                interface.custom_error(e)
        if args.u_new:
            try:
                interface.create_user(takeaway.user.create_user(args.u_new))
            except UserError as e:
                interface.custom_error(e)
        if args.u_list:
            interface.list_users(takeaway.database.get_users())
        # Database call
        if args.db_list:
            interface.db_list(takeaway.database.list_postcode(country=args.db_list))
        elif args.db_del:
            try:
                interface.db_delete(takeaway.database.delete_postcode(args.db_del[0], args.db_del[1]),
                                    args.db_del[0], args.db_del[1])
            except DatabaseError as e:
                interface.custom_error(e)
        elif args.db_make:
            try:
                interface.db_make(takeaway.make_database(output=True))
            except KeyboardInterrupt as e:
                interface.error(e)
        elif args.db_update is not False:
            try:
                if args.db_update is True:
                    interface.db_update(takeaway.update_database(output=True))
                elif args.db_update >= 0:
                    interface.db_update(takeaway.update_database(output=True, days=args.db_update))
                else:
                    interface.print("Error with --db-update arguments. Number of days must be >= 0.")
            except ScrapperError as e:
                interface.custom_error(e)
        elif args.db_consolidate:
            try:
                interface.db_consolidate(takeaway.consolidate_database(output=True))
            except ScrapperError as e:
                interface.custom_error(e)

        # Search call
        if args.search_meal is not False or args.search_cat is not False or args.search_rest is not False:
            if args.search_meal == list():
                args.search_meal = True
            if args.search_cat == list():
                args.search_cat = True
            if args.search_rest == list():
                args.search_rest = True
            rep, rep_type = takeaway.database.search(args.search_meal, args.search_cat, args.search_rest, args.time)
            if not args.checkout:
                if len(rep) == 0:
                    interface.print("No result found for this query.")
                elif rep_type == "restaurant":
                    interface.print_restaurant(rep, args.verbose)
                elif rep_type == "category":
                    interface.print_category(rep)
                elif rep_type == "meal":
                    interface.print_meal(rep)

        # Basket call
        if args.ba_clear:
            interface.clear_basket(takeaway.basket.delete_all())
        if args.ba_add:
            try:
                interface.add_basket(takeaway.basket.add(args.ba_add))
            except BasketError as e:
                interface.custom_error(e)
        if args.ba_del:
            try:
                interface.del_basket(takeaway.basket.delete(args.ba_del))
            except BasketError as e:
                interface.custom_error(e)
        if args.ba_list:
            interface.print_basket(takeaway.basket.items)

        # Checkout
        if args.checkout:
            try:
                interface.checkout(takeaway.checkout(args.checkout, args.confirm))
            except BasketError as e:
                interface.custom_error(e)
            except ScrapperError as e:
                interface.custom_error(e)

        # Interactive
        if args.interactive:
            break
			
def get_input(takeaway, interface):
    """
    Request commands input from user (interactive mode)
    :return: list of string from user input
    """
    user_input_basket = ""  # Basket info to display
    user_input_user = ""  # User info to display
    user_input_postcode = "Postcode: {} {}\n".format(takeaway.database.postcode.country,
                                                     takeaway.database.postcode.postcode)
    if takeaway.basket.total:  # If total is not 0
        user_input_basket = "Total: {} euros\n".format(takeaway.basket.total)
    if takeaway.user.user:  # If a user is loaded
        user_input_user = "User: {}\n".format(takeaway.user.user.username.title())

    u_input_raw = interface.input(
        "\n{}{}{}(-i to quit) Command: ".format(user_input_user, user_input_postcode, user_input_basket))

    # Clean user input to be parse with argparse
    logging.debug("Raw user input: {}".format(u_input_raw))
    u_input_raw = re.findall('\'[^\']*\'|\"[^\"]*\"|\S+', u_input_raw)  # Split the string (keep bracket together)
    # Clean string (add country/postcode as first args)
    u_input = [takeaway.database.postcode.country, takeaway.database.postcode.postcode]
    for string in u_input_raw:
        string = string.replace('"', "").replace("'", "")  # Delete " and ' from raw string
        u_input.append(string)  # Add clean string to u_input
    logging.debug("Clean user input: {}".format(u_input))

    return u_input  # Output clean reformatted string

if __name__ == "__main__":
    main()