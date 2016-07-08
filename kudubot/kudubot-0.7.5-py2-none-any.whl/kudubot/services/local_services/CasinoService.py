# coding=utf-8
u"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of kudubot.

    kudubot makes use of various third-party python modules to serve
    information via online chat services.

    kudubot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    kudubot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with kudubot.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
from __future__ import division
from __future__ import with_statement
from __future__ import absolute_import
import os
import re
import time
import random
import datetime
from typing import Dict, List

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message
from kudubot.config.LocalConfigChecker import LocalConfigChecker
from io import open


class CasinoService(Service):
    u"""
    The CasinoService Class that extends the generic Service class.
    The service provides the backbone for all casino-related services, like the Roulette Service
    Note: All monetary values are in cents
    """

    identifier = u"casino"
    u"""
    The identifier for this service
    """

    has_background_process = True
    u"""
    Has a backround process
    """

    help_description = {u"en": u"/casino\tprovides basic casino functions\n"
                              u"syntax:\n"
                              u"/casino balance\tsends you your current balance\n"
                              u"/casino beg\tlets you beg for money",
                        u"de": u"/casino\tBietet simple Casino Funktionen\n"
                              u"syntax:\n"
                              u"/casino kontostand\tSchickt den momentanen Kontostand des Nutzers\n"
                              u"/casino betteln\tLässt den Nutzer für Geld betteln"}
    u"""
    Help description for this service.
    """

    casino_directory = u""
    u"""
    The directory containing the casino files
    """

    user_directory = u""
    u"""
    The directory storing user account files
    """

    bet_directory = u""
    u"""
    The directory storing user bets
    """

    currency = u"€"
    u"""
    The currency used
    """

    account_balance_keywords = {u"balance": u"en",
                                u"kontostand": u"de"}
    u"""
    Keywords for the account balance parameter
    """

    beg_keyword = {u"beg": u"en",
                   u"betteln": u"de"}
    u"""
    Keywords for the beg command
    """

    beg_values = [50, 100, 200, 300, 400, 500, 30000]
    u"""
    Monetary Values that can be gained with begging
    """

    beg_message = {u"en": (u"You beg for money. You earn ", u" while begging"),
                   u"de": (u"Du bettelst für Geld. Du verdienst ", u" während dem Betteln")}
    u"""
    Message sent to the user if he/she begs
    """

    balance_message = {u"en": u"Your account balance is: ",
                       u"de": u"Dein Kontostand beträgt: "}
    u"""
    Message shown when the user requests his/her account balance
    """

    no_bets_stored = {u"en": u"No bets stored",
                      u"de": u"Keine Wetten gespeichert"}
    u"""
    Message shown when no bets are stored
    """

    delete_bet_out_of_bound = {u"en": u"No bet with that index available",
                               u"de": u"Keine Wette mit dem Index verfügbar"}
    u"""
    Message shown if the user tries to delete a message at an invalid index
    """

    successful_bet_delete_message = {u"en": u"Bet successfully deleted",
                                     u"de": u"Wette erfolgreich gelöscht"}
    u"""
    Message shown when a bet was successfully deleted
    """

    bet_stored_message = {u"en": u"The bet was successfully stored",
                          u"de": u"Die Wette wurde erfolgreich gespeichert"}
    u"""
    Message shown when a bet was stored successfully
    """

    insufficient_funds_message = {u"en": u"Insufficient Funds for the placed bet",
                                  u"de": u"Ungenügendes Guthaben für diese Wette"}
    u"""
    Message shown when the user tries to store a bet of a value higher than his/her account balance
    """

    def initialize(self):
        u"""
        Initializes the casino directories

        :return: None
        """
        self.casino_directory = os.path.join(LocalConfigChecker.services_directory,
                                             self.connection.identifier, u"casino")
        self.user_directory = os.path.join(self.casino_directory, u"users")
        self.bet_directory = os.path.join(self.casino_directory, u"bets")

        LocalConfigChecker.validate_directory(self.casino_directory)
        LocalConfigChecker.validate_directory(self.user_directory)
        LocalConfigChecker.validate_directory(self.bet_directory)

    def process_message(self, message):
        u"""
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        address = message.get_individual_address()
        option = message.message_body.lower().split(u"/casino ")[1]
        reply = u""

        if option in self.beg_keyword:
            self.connection.last_used_language = self.beg_keyword[option]
            reply = self.beg(address)
        elif option in self.account_balance_keywords:
            self.connection.last_used_language = self.account_balance_keywords[option]
            reply = self.get_balance_as_message(address)

        reply_message = self.generate_reply_message(message, u"Casino", reply)
        self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message):
        u"""
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = u"^/casino " + Service.regex_string_from_dictionary_keys([CasinoService.beg_keyword,
                                                                         CasinoService.account_balance_keywords]) + u"$"
        return re.search(re.compile(regex), message.message_body.lower())

    def beg(self, address):
        u"""
        Executes the 'beg' command, giving the user a random amount(mostly small) of money to gamble with

        :param address: the address for the user
        :return: A reply message for the user
        """
        beg_amount = random.choice(self.beg_values)
        response = self.beg_message[self.connection.last_used_language]

        self.transfer_funds(address, beg_amount)
        return response[0] + self.format_money_string(beg_amount) + response[1]

    def get_balance_as_message(self, address):
        u"""
        Gets the current balance of the user

        :param address: the unique address
        :return: the message to be sent to the user
        """
        try:
            balance = self.get_balance(address)
        except FileNotFoundError:
            self.create_account(address)
            balance = self.get_balance(address)

        response = self.balance_message[self.connection.last_used_language]

        return response + self.format_money_string(int(balance))

    def create_account(self, address, starting_value = 200000):
        u"""
        Creates a new user account

        :param address: the user address for whom the account is created
        :param starting_value: can be used to set a custom starting value
        :return: None
        """
        account_file = os.path.join(self.user_directory, address)
        with open(account_file, u'w') as account:
            account.write(unicode(starting_value))

    def transfer_funds(self, address, amount):
        u"""
        Transfers funds to/from an account
        It can be called with negative values to remove money from the account

        :param address: the user's address
        :param amount: the amount to transfer
        :return: None
        """
        user_exists = False
        for user_file in os.listdir(self.user_directory):
            if user_file.startswith(address):
                account_file = os.path.join(self.user_directory, user_file)

                user_exists = True
                current_balance = self.get_balance(address)

                if current_balance + amount < 0:
                    raise InsufficientFundsError()
                else:
                    with open(account_file, u'w') as account:
                        account.write(unicode(current_balance + amount))

        if not user_exists:
            self.create_account(address)
            if amount >= -200000:
                self.transfer_funds(address, amount)
            else:
                raise InsufficientFundsError()

    def get_balance(self, address):
        u"""
        Reads the current balance from the account file

        :param address: the user address
        :return: the account balance.
        """
        account_file = os.path.join(self.user_directory, address)
        with open(account_file, u'r') as account:
            account_balance = int(account.read())
        return account_balance

    def format_money_string(self, value):
        u"""
        Formats a cent-based monetary value into a human-readable string

        :param value: the value to be formatted
        :return: the formatted money string
        """
        cents = value % 100
        dollars = int((value - cents) / 100)

        cent_string = unicode(cents) if cents > 9 else u"0" + unicode(cents)
        return unicode(dollars) + u"," + cent_string + self.currency

    def parse_money_string(self, money_string):
        u"""
        Reads a money string and returns its value as a cent-based int value

        :param money_string: the string to be parsed
        :return: the value of that string
        """
        money_string = money_string.replace(u".", u",")
        money = money_string.replace(self.currency, u"")
        money = money.split(u",")

        dollars = money[0]
        cents = 0 if len(money) < 2 else money[1]

        value = int(cents) + (int(dollars) * 100)

        return value

    def store_bet(self, game, address, value, bet_type):
        u"""
        Stores a bet as a bet file

        :param game: the game this bet was created by
        :param address: the address of the better
        :param value: the value set
        :param bet_type: the bet type - game-specific
        :return: a confirmation message if everything went well, an insufficient funds message if not
        """
        try:
            self.transfer_funds(address, -value)
            directory = os.path.join(self.bet_directory, game)
            file_name = address + u"###BETVAL=" + bet_type
            bet_file = os.path.join(directory, file_name)

            if os.path.isfile(bet_file):
                with open(bet_file, u'r') as bet:
                    value = int(bet.read())
                    value *= 2

            with open(bet_file, u'w') as bet:
                bet.write(unicode(value))

            return self.bet_stored_message[self.connection.last_used_language]
        except InsufficientFundsError:
            return self.insufficient_funds_message[self.connection.last_used_language]

    def get_bets(self, game, address):
        u"""
        Returns a list of dictionaries representing bets of a specific user

        :param game: the game for which the bets should be fetched
        :param address: the user's address
        :return: the List of reminder dictionaries
        """
        directory = os.path.join(self.bet_directory, game)
        bets = []

        for bet in os.listdir(directory):
            if bet.startswith(address):
                bet_file = os.path.join(directory, bet)

                bet_dictionary = {u"bet_type": bet.rsplit(u"###BETVAL=", 1)[1],
                                  u"file": bet_file,
                                  u"user": bet.rsplit(u"###BETVAL=", 1)[0],
                                  u"address": bet.rsplit(u"###BETVAL=", 1)[0]}

                with open(bet_file, u'r') as opened_bet_file:
                    bet_dictionary[u"value"] = int(opened_bet_file.read())

                bets.append(bet_dictionary)

        bets = sorted(bets, key=lambda dictionary: dictionary[u"value"])
        return bets

    def get_bets_as_formatted_string(self, game, address):
        u"""
        Return all bets of a user for a specific game as a formatted string

        :param game: the game to which the bets belong
        :param address: the user's address
        :return: the formatted string
        """
        bets = self.get_bets(game, address)
        bet_list_string = u""

        for bet in xrange(0, len(bets)):
            bet_list_string += unicode(bet + 1) + u": "
            bet_list_string += self.format_money_string(bets[bet][u"value"]) + u"\n"
            bet_list_string += bets[bet][u"bet_type"] + u"\n\n"

        if bet_list_string == u"":
            bet_list_string = self.no_bets_stored[self.connection.last_used_language]
        else:
            bet_list_string = bet_list_string.rsplit(u"\n\n", 1)[0]

        return bet_list_string

    def delete_bet(self, game, address, index):
        u"""
        Deletes a bet at the given iundex for the given game by the given user

        :param game: the game the bet to delete belongs to
        :param address: the user's address
        :param index: the index of the bet to delete
        :return: A message to the user
        """
        if index < 1:
            return self.delete_bet_out_of_bound[self.connection.last_used_language]

        bets = self.get_bets(game, address)
        os.remove(bets[index - 1][u'file'])

        return self.successful_bet_delete_message[self.connection.last_used_language]

    def background_process(self):
        u"""
        Adds 100 € each day to each account

        :return: None
        """
        while True:
            current_time = datetime.datetime.utcnow()
            hour = int(current_time.hour)

            if hour == 23:
                for account_file in os.listdir(self.user_directory):
                    user_address = unicode(account_file.rsplit(u"###BETVAL=", 1)[0])
                    self.transfer_funds(user_address, 10000)
            time.sleep(3600)


class InsufficientFundsError(Exception):
    u"""
    Error to be raised when insufficient funds
    """
    pass
