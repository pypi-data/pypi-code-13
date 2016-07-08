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
from __future__ import absolute_import
import os
import re
import time
import calendar
import datetime
from typing import Tuple, Dict, List

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message
from kudubot.config.LocalConfigChecker import LocalConfigChecker
from io import open


class ReminderService(Service):
    u"""
    The ReminderService Class that extends the generic Service class.
    The service offers reminder at specific or relative times
    """

    identifier = u"reminder"
    u"""
    The identifier for this service
    """

    help_description = {u"en": u"/remind\tSaves a reminder and sends it back at the specified time\n"
                              u"syntax: /remind \"<message>\" <time>\n"
                              u"time syntax: <YYYY-MM-DD-hh-mm-ss>\n"
                              u"or: <amount> [years|months|days|hours|minutes|seconds]\n"
                              u"or: tomorrow\n\n"
                              u"/remind list\tLists all reminders currently stored\n"
                              u"/remind delete <index>\tDeletes the reminder at the given index\n\n"
                              u"All times are stored in UTC",
                        u"de": u"/remind\tSpeichert eine Erinnerung und verschickt diese zum angegebenen Zeitpunkt\n"
                              u"syntax: /erinner \"<nachricht>\" <zeit>\n"
                              u"zeit syntax: YYYY-MM-DD-hh-mm-ss\n"
                              u"oder: <anzahl> [jahre|monate|tage|stunden|minuten|sekunden]\n"
                              u"oder: morgen\n\n"
                              u"/erinner list\tListet alle Erinnerungen\n"
                              u"/erinner delete <index>\tDeletes the reminder at the given index\n\n"
                              u"Alle Zeiten werden in UTC gespeichert"}
    u"""
    Help description for this service.
    """

    has_background_process = True
    u"""
    Indicates that the serice has a background process
    """

    message_stored_reply = {u"en": u"Message Stored",
                            u"de": u"Nachricht gespeichert"}
    u"""
    Reply to signal the user that the reminder was successfully stored
    """

    reminder_directory = u"reminder"
    u"""
    The directory in which the reminders are stored
    """

    remind_keywords = {u"remind": u"en",
                       u"erinner": u"de"}
    u"""
    Keywords for the remind command
    """

    time_adder_keywords = {u"years": [u"en", u"years"],
                           u"jahre": [u"de", u"years"],
                           u"months": [u"en", u"months"],
                           u"monate": [u"de", u"months"],
                           u"days": [u"en", u"days"],
                           u"tage": [u"de", u"days"],
                           u"hours": [u"en", u"hours"],
                           u"stunden": [u"de", u"hours"],
                           u"minutes": [u"en", u"minutes"],
                           u"minuten": [u"de", u"minutes"],
                           u"seconds": [u"en", u"seconds"],
                           u"sekunden": [u"de", u"seconds"]}
    u"""
    Keywords for specific time sizes
    """

    tomorrow_keywords = {u"tomorrow": u"en",
                         u"morgen": u"de"}
    u"""
    Keywords that define the tomorrow option
    """

    remider_time = {u"years": 0,
                    u"months": 0,
                    u"days": 0,
                    u"hours": 0,
                    u"minutes": 0,
                    u"seconds": 0}
    u"""
    The time when the reminder shoul be activated
    """

    list_keywords = {u"list": u"en",
                     u"liste": u"de"}
    u"""
    Keywords for the list command
    """

    no_reminders_stored = {u"en": u"No reminders stored",
                           u"de": u"Keine Erinnerungen gespeichert"}
    u"""
    Message sent if the user requests a list of his reminders, but there are none
    """

    reminder_delete_out_of_bounds = {u"en": u"No reminder with that index stored",
                                     u"de": u"Keine Erinnerung mit diesem Index."}
    u"""
    Message sent when the delete command's index is out of bounds
    """

    delete_file_success = {u"en": u"Successfully deleted reminder",
                           u"de": u"Erinnerung erfolgreich gelöscht"}
    u"""
    Success message when deleting an reminder
    """

    delete_keywords = {u"delete": u"en",
                       u"löschen": u"de"}
    u"""
    Keywords for the delete command
    """

    def initialize(self):
        u"""
        Constructor extender for the Renamer class that initializes a directory for the reminder files

        :return: None
        """
        self.reminder_directory = \
            os.path.join(LocalConfigChecker.services_directory, self.connection.identifier, self.reminder_directory)
        LocalConfigChecker.validate_directory(self.reminder_directory)

    def process_message(self, message):
        u"""
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        user_input = message.message_body.lower()
        delete_key = None
        for key in self.delete_keywords:
            if key in user_input:
                delete_key = key
        list_key = None
        for key in self.list_keywords:
            if key in user_input:
                list_key = key

        if delete_key is not None:  # In other words: if "delete" in message.message_body.lower()
            language = self.delete_keywords[delete_key]
            index = int(message.message_body.split(delete_key + u" ")[1])
            reply = self.delete_reminder_for_user(message.address, index, language)

        elif list_key is not None:
            language = self.list_keywords[list_key]
            reply = self.get_user_reminders_as_string_from(message.address, language)

        else:
            language, reminder_options, reminder_message = self.parse_user_input(message.message_body)
            reminder_time = self.determine_reminder_time(reminder_options)
            reminder_time = self.normalize_time(reminder_time)

            self.store_reminder(reminder_time, reminder_message, message.address)
            reply = self.message_stored_reply[language]

        reply_message = self.generate_reply_message(message, u"Reminder", reply)
        self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message):
        u"""
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = u"^/" + Service.regex_string_from_dictionary_keys([ReminderService.remind_keywords])
        regex += u" \"[^\"]+\" ([0-9]+ " + \
                 Service.regex_string_from_dictionary_keys([ReminderService.time_adder_keywords])
        regex += u"|" + Service.regex_string_from_dictionary_keys([ReminderService.tomorrow_keywords])
        regex += u"|[0-9]{4}-[0-9]{2}-[0-9]{2}(-[0-9]{2}-[0-9]{2}-[0-9]{2})?)$"

        list_regex = u"^/" + Service.regex_string_from_dictionary_keys([ReminderService.remind_keywords]) + u" "
        list_regex += Service.regex_string_from_dictionary_keys([ReminderService.list_keywords]) + u"$"

        delete_regex = u"^/" + Service.regex_string_from_dictionary_keys([ReminderService.remind_keywords]) + u" "
        delete_regex += Service.regex_string_from_dictionary_keys([ReminderService.delete_keywords]) + u" [0-9]+$"

        return re.search(re.compile(regex), message.message_body.lower())\
            or re.search(re.compile(list_regex), message.message_body.lower())\
            or re.search(re.compile(delete_regex), message.message_body.lower())

    def parse_user_input(self, user_input):
        u"""
        Parses the user input and determines the used language, the reminder to be stored,
        as well as th options defining when the reminder will be activated

        :param user_input: the user input to be parsed
        :return: language, options, reminder text
        """

        remind_keyword, options = user_input.split(u" ", 1)  # Split message into /remind and the rest of the message
        language = self.remind_keywords[remind_keyword.lower().split(u"/")[1]]  # Get the language using /remind keyword

        # Split message into three parts:
        # junk: empty string, stuff that comes before the first quotation mark
        # reminder_message: The message nested between quotation marks
        # options: the options after the reminder string
        junk, reminder_message, options = options.split(u"\"", 2)

        options = options.lower().lstrip()  # Remove leading whitespace

        return language, options, reminder_message

    def determine_reminder_time(self, options):
        u"""
        Determines the reminder time from the given options

        :param options: the options to be parsed
        :return: the reminder time as a dictionary
        """
        reminder_time = self.get_time()

        if options in self.tomorrow_keywords:
            reminder_time[u"days"] += 1

        elif re.search(ur"[0-9]{4}-[0-9]{2}-[0-9]{2}(-[0-9]{2}-[0-9]{2}-[0-9]{2})?", options):
            selected_time = options.split(u"-")
            reminder_time[u"years"] = int(selected_time[0])
            reminder_time[u"months"] = int(selected_time[1])
            reminder_time[u"days"] = int(selected_time[2])
            if len(selected_time) > 3:
                reminder_time[u"hours"] = int(selected_time[3])
                reminder_time[u"minutes"] = int(selected_time[4])
                reminder_time[u"seconds"] = int(selected_time[5])

        else:
            modifier, key = options.split(u" ")
            reminder_time[key] += int(modifier)

        return reminder_time

    def store_reminder(self, reminder_time, reminder_message, reminder_address):
        u"""
        Stores a reminder in the reminder directory as a reminder file.

        :param reminder_time: the time the reminder activates
        :param reminder_message: the reminder text itself
        :param reminder_address: the address to where the reminder will be sent
        :return: None
        """
        timestamp = ReminderService.convert_time_to_utc_timestamp(reminder_time)

        # emulate a do-while loop
        # The loop makes sure that no existing file is overwritten
        counter = 0
        while True:
            reminder_filename = unicode(timestamp) + u"#" + unicode(counter) + u"@" + reminder_address
            reminder_file = os.path.join(self.reminder_directory, reminder_filename)
            if not os.path.isfile(reminder_file):
                break
            else:
                counter += 1

        # Disable inspection because the loop will run at least once
        # noinspection PyUnboundLocalVariable
        opened_file = open(reminder_file, u'w')
        opened_file.write(reminder_message)
        opened_file.close()

    @staticmethod
    def get_time(timestamp = None):
        u"""
        Returns the current time as a dicitonary, or optionally gets the time from a UTC timestamp

        :param timestamp: Optional timestamp
        :return: the time dictionary
        """
        if timestamp is None:
            date_time_object = datetime.datetime.utcnow()
        else:
            date_time_object = datetime.datetime.utcfromtimestamp(timestamp)
        return {u"years": date_time_object.year,
                u"months": date_time_object.month,
                u"days": date_time_object.day,
                u"hours": date_time_object.hour,
                u"minutes": date_time_object.minute,
                u"seconds": date_time_object.second}

    @staticmethod
    def normalize_time(time_dictionary):
        u"""
        Normalizes a time dictionary (seconds to max 60, months to max 12 etc.)

        :param time_dictionary: the time dictionary to be normalized
        :return: the normalized time dictionary
        """

        def transfer_overdraft(smaller_unit, larger_unit, limit):
            u"""
            Transfers an overdraft to the next biggest unit

            :param smaller_unit: the value of the smaller unit
            :param larger_unit: the value of the larger unit
            :param limit: the limit of the smaller unit
            :return: the new smaller and largr unit values as a Tuple
            """

            extra_larger_unit = int((smaller_unit - smaller_unit % limit) / limit)
            smaller_unit %= limit
            larger_unit += extra_larger_unit

            return smaller_unit, larger_unit

        def get_month_length():
            u"""
            Calculates the length of a the currently selected month of the time dictionary

            :return: the amount of days in that month
            """
            if time_dictionary[u"months"] in [1, 3, 5, 7, 8, 10, 12]:
                return 31
            elif time_dictionary[u"months"] in [4, 6, 9, 11]:
                return 30
            elif time_dictionary[u"months"] == 2 and time_dictionary[u"years"] % 4 == 0:
                return 29
            else:
                return 28

        def increment_month():
            u"""
            Increments the month of the time dictionary by 1

            :return: the incremented dictionary
            """
            if time_dictionary[u"months"] == 12:
                time_dictionary[u"months"] = 1
                time_dictionary[u"years"] += 1
            else:
                time_dictionary[u"months"] += 1

        time_dictionary[u"seconds"], time_dictionary[u"minutes"] =\
            transfer_overdraft(time_dictionary[u"seconds"], time_dictionary[u"minutes"], 60)

        time_dictionary[u"minutes"], time_dictionary[u"hours"] = \
            transfer_overdraft(time_dictionary[u"minutes"], time_dictionary[u"hours"], 60)

        time_dictionary[u"hours"], time_dictionary[u"days"] = \
            transfer_overdraft(time_dictionary[u"hours"], time_dictionary[u"days"], 24)

        time_dictionary[u"months"], time_dictionary[u"years"] = \
            transfer_overdraft(time_dictionary[u"months"], time_dictionary[u"years"], 12)

        month_length = get_month_length()
        while time_dictionary[u"days"] > month_length:
            time_dictionary[u"days"] -= month_length
            increment_month()
            month_length = get_month_length()

        return time_dictionary

    @staticmethod
    def convert_time_to_utc_timestamp(time_dict):
        u"""
        Converts a time dictionary to a UTC time stamp, rounded to seconds

        :param time_dict: the time dictionary to be converted
        :return: the timestamp
        """

        date = unicode(time_dict[u"years"]) + u"-" + unicode(time_dict[u"months"]) + u"-" + unicode(time_dict[u"days"]) + u":"
        date += unicode(time_dict[u"hours"]) + u"-" + unicode(time_dict[u"minutes"]) + u"-" + unicode(time_dict[u"seconds"])
        date = time.strptime(date, u"%Y-%m-%d:%H-%M-%S")

        return int(calendar.timegm(date))

    # noinspection PyTypeChecker
    def list_reminders_of(self, sender):
        u"""
        Lists all reminders of a user and the times they will be sent

        :param sender: the sender to check reminder files for
        :return: an indexed list of reminders
        """
        user_reminders = []
        for reminder_file_name in os.listdir(self.reminder_directory):

            if sender in reminder_file_name:
                reminder_file = os.path.join(self.reminder_directory, reminder_file_name)
                opened_file = open(reminder_file, u'r')

                reminder_due_time = int(reminder_file_name.split(u"#", 1)[0])
                reminder_text = opened_file.read()
                opened_file.close()

                user_reminders.append({u"time": unicode(reminder_due_time),
                                       u"text": reminder_text,
                                       u"file": reminder_file})

        return sorted(user_reminders, key=lambda dictionary: dictionary[u"time"])

    def get_user_reminders_as_string_from(self, sender, language):
        u"""
        Creates a string that lists all currently active reminders of a specific user

        :param sender: the sender to check
        :param language: The language to send the reply in
        :return: the generated string
        """
        reminders = self.list_reminders_of(sender)
        list_string = u""

        for index in xrange(1, len(reminders) + 1):
            # noinspection PyTypeChecker
            time_dict = self.get_time(int(reminders[index - 1][u'time']))

            list_string += unicode(index) + u": "
            list_string += unicode(time_dict[u'years']) + u"-" + unicode(time_dict[u'months']) + u"-" + unicode(time_dict[u'days'])
            list_string += u":"
            list_string += unicode(time_dict[u'hours']) + u"-" + unicode(time_dict[u'minutes']) + u"-" + unicode(time_dict[u'seconds'])
            list_string += u"\n"
            list_string += reminders[index - 1][u'text']

            if index != len(reminders):
                list_string += u"\n\n"

        if not list_string:
            list_string = self.no_reminders_stored[language]

        return list_string

    def delete_reminder_for_user(self, user, reminder_to_delete_index, language):
        u"""
        Deletes a stored reminder and returns the result of the deletion.

        :param user: the user whose reminder that is
        :param reminder_to_delete_index: the index for the reminder to delete
        :param language: The language in which the reply should be sent
        :return: the reply to the user
        """
        try:
            reminder = self.list_reminders_of(user)[reminder_to_delete_index - 1]
            os.remove(reminder[u'file'])
            return self.delete_file_success[language]
        except IndexError:
            return self.reminder_delete_out_of_bounds[language]

    def background_process(self):
        u"""
        Background process that checks for due reminders and sends them to the sender if they are.

        :return: None
        """
        while True:

            for reminder_file_name in os.listdir(self.reminder_directory):
                reminder_file = os.path.join(self.reminder_directory, reminder_file_name)

                reminder_due_time = int(reminder_file_name.split(u"#", 1)[0])
                current_time = int(time.time())

                if current_time >= reminder_due_time:
                    receiver = reminder_file_name.split(u"@", 1)[1]

                    opened_file = open(reminder_file, u'r')
                    message_text = opened_file.read()
                    opened_file.close()
                    os.remove(reminder_file)

                    # noinspection PyTypeChecker
                    message = Message(message_text, u"Reminder", receiver, False)

                    self.connection.send_text_message(message)

            time.sleep(1)
