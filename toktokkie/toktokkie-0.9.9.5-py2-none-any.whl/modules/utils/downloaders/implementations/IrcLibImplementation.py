u"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    toktokkie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    toktokkie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with toktokkie.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
from __future__ import division
from __future__ import absolute_import
import os
import random
import shlex
import struct
import sys
import time
import irc.client
from typing import List
from puffotter.stringformatter import ForegroundColors, BackgroundColors, print_formatted_string
from toktokkie.modules.objects.ProgressStruct import ProgressStruct
from jaraco.stream import buffer
from io import open


# This construct ignores all non-decodeable received strings
class IgnoreErrorsBuffer(buffer.DecodingLineBuffer):
    def handle_exception(self):
        pass
irc.client.ServerConnection.buffer_class = IgnoreErrorsBuffer
irc.client.SimpleIRCClient.buffer_class = IgnoreErrorsBuffer


class IrcLibImplementation(irc.client.SimpleIRCClient):
    u"""
    This class extends the SimpleIRCClient Class to download XDCC packs using the irclib library
    It is based on the tutorial scripts on the library's Github page, but strongly modified to suit the
    needs of the batch download manager.
    """

    server = u""
    u"""
    The server address of the server the downloader has to connect to.
    """

    bot = u""
    u"""
    The bot serving the requested file
    """

    pack = -1
    u"""
    The pack number of the file to be downloaded
    """

    destination_directory = u""
    u"""
    The directory to which the file should be downloaded to
    """

    nickname = u""
    u"""
    A nickname for the bot
    """

    progress_struct = None
    u"""
    A progress struct to share the download progress between threads
    """

    filename = u""
    u"""
    The path to the downloaded file
    """

    file = None
    u"""
    The downloaded file opened for writing
    """

    dcc = None
    u"""
    The established DCC connection to the file server bot
    """

    time_counter = int(time.time())
    u"""
    Keeps track of the time to control how often status updates about the download are printed to the console
    """

    common_servers = [u"irc.rizon.net", u"irc.criten.net", u"irc.scenep2p.net", u"irc.freenode.net", u"irc.abjects.net"]
    u"""
    A list of common servers to try in case a bot does not exist on a server
    """

    server_retry_counter = 0
    u"""
    Counter for server retries
    """

    connection_started = False
    u"""
    Flag that is set to true while a connection is in progress
    """

    bot_requires_channel_join = False
    u"""
    Flag that gets set if the bot resides in one or more channels
    """

    joined_channel = False
    u"""
    Flag that gets set when the bot successfully enters a channel
    """

    download_started = False
    u"""
    Flag that gets set once the download starts
    """

    start_time = time.time()
    u"""
    Timestamp to calculate if a timeout occurred in the onping() method
    """

    verbosity_level = 0
    u"""
    Defines how verbose the logging will be printed to the console.
    Verbosity Level 0 prints nothing
    """

    def __init__(self, server, bot, pack, destination_directory, progress_struct,
                 file_name_override = None, verbosity_level = 0):
        u"""
        Constructor for the IrcLibImplementation class. It initializes the base SimpleIRCClient class
        and stores the necessary information for the download process as class variables

        :param server: The server to which the Downloader needs to connect to
        :param bot: The bot serving the file to download
        :param pack: The pack number of the file to download
        :param destination_directory: The destination directory of the downloaded file
        :param progress_struct: The progress struct to keep track of the download progress between threads
        :param file_name_override: Can be set to pre-determine the file name of the downloaded file
        :param verbosity_level: The level of verbosity to run the XDCC downloader with
        :return: None
        """
        # Initialize base class
        super(IrcLibImplementation, self).__init__()

        # Store values
        self.server = server
        self.bot = bot
        self.pack = pack
        self.destination_directory = destination_directory
        self.progress_struct = progress_struct
        self.verbosity_level = verbosity_level

        # Remove the server from common server list if it is included there
        try:
            self.common_servers.remove(server)
        except ValueError:
            pass

        # If a file name is pre-defined, set the file name to be that name.
        if file_name_override is not None:
            self.filename = os.path.join(destination_directory, file_name_override)

    def log(self, string, priority, formatting = None):
        u"""
        Prints a string, if the verbose option is set

        :param string: the string to print
        :param priority: For which verbosity level this log should be printed
        :param formatting: optional formatting options for the string used with puffotter's string formatter
        :return: None
        """
        if self.verbosity_level >= priority:
            if formatting is None:
                print string
            else:
                print_formatted_string(string, formatting)

    def connect(self):
        u"""
        Connects to the server with a randomly generated username
        :return: None
        """
        self.nickname = u"media_manager_python" + unicode(random.randint(0, 1000000))  # Generate random nickname
        self.log(u"Connecting to server " + self.server + u" at port 6667 as user " + self.nickname, 2,
                 ForegroundColors.WHITE)
        super(IrcLibImplementation, self).connect(self.server, 6667, self.nickname)  # Connect to server

    def start(self):
        u"""
        Starts the download process and returns the file path of the downloaded file once the download completes
        :return: the path to the downloaded file
        """
        success = False
        self.log(u"Starting Download", 2, ForegroundColors.WHITE)
        self.connection_started = False
        while not self.connection_started:
            self.connection_started = True
            try:
                self.connect()  # Connect to server
                super(IrcLibImplementation, self).start()  # Start the download

            except ConnectionAbortedError:  # Bot not found on current server
                try:
                    self.server = self.common_servers[self.server_retry_counter]
                    self.server_retry_counter += 1
                    self.reset_state()
                    self.log(u"Trying different server...", 2, ForegroundColors.RED)

                except IndexError:  # Went through list of servers, could not find a match
                    raise ConnectionError(u"Failed to find the bot on any known server")

            except SystemExit:  # Fallback in case the self.connection.quit() call failed
                success = True
            except ConnectionError:  # Bot not found on any known server
                pass

            if success:
                self.log(u"Download completed Successfully", 1)
            else:
                self.log(u"Download did not complete successfully.", 1)

            if not self.progress_struct.single_progress == self.progress_struct.single_size:
                self.log(u"WARNING: Progress does not match file size", 5, ForegroundColors.LIGHT_RED)
                self.log(u"PROGRESS: " + unicode(self.progress_struct.single_progress), 5, ForegroundColors.LIGHT_GRAY)
                self.log(u"SIZE    : " + unicode(self.progress_struct.single_size), 5, ForegroundColors.LIGHT_GRAY)

            # Check that the complete file was downloaded
            if self.progress_struct.single_progress < self.progress_struct.single_size:
                self.log(u"Download not completed successfully, trying again", 2, ForegroundColors.RED)
                self.reset_state()

        return self.filename  # Return the file path

    def reset_state(self):
        u"""
        Resets the state of the downloader (deletes previously downloaded file, resets progress struct)
        :return: None
        """
        self.connection_started = False
        self.bot_requires_channel_join = False
        self.joined_channel = False
        self.download_started = False
        if os.path.isfile(self.filename):
            os.remove(self.filename)
        self.progress_struct.single_progress = 0

    def on_ping(self, connection, event):
        u"""
        Checks for timeouts
        :param connection: the IRC connection
        :param event: the notice event
        :return: None
        """
        if connection is None:
            pass

        current_time = time.time()
        time_delta = current_time - self.start_time
        if not self.download_started and time_delta > 120.0:
            self.log(u"TIMEOUT: Aborting", 1, ForegroundColors.LIGHT_RED)
            event.arguments[0] = u"TIMEOUT"
            self.on_disconnect(connection, event)

    def on_welcome(self, connection, event):
        u"""
        Method run when the IRCClient successfully connects to a server. It sends a whois request
        to find out which channel to join

        :param connection: The IRC connection
        :param event: The event that caused this method to be run
        :return: None
        """
        # Make Pycharm happy
        if event is None:
            return
        self.log(u"Connection to server " + self.server + u" established. Sending WHOIS command for " + self.bot, 2,
                 ForegroundColors.WHITE)
        connection.whois(self.bot)

    def on_nosuchnick(self, connection, event):
        u"""
        Checks if there exists a bot with the specified name on the server

        :param connection: the IRC connection
        :param event: the nosuchnick event
        :return: None
        """
        self.bot_requires_channel_join = True
        self.log(u"NOSUCHNICK", 2, ForegroundColors.RED)
        if connection is None:
            pass
        if event.arguments[0] == self.bot:
            connection.disconnect(u"Bot does not exist on server")

    def on_endofwhois(self, connection, event):
        u"""
        Checks the end of a WHOIS command if a channel join has occured or was even necessary
        If it was not necessary, starts the download

        :param connection: the IRC connection
        :param event: the endofwhois event
        :return: None
        """
        if not self.bot_requires_channel_join:
            event.source = self.nickname
            self.on_join(connection, event)

    def on_whoischannels(self, connection, event):
        u"""
        Checks the channels the bot is connected to.

        :param connection: the IRC connection
        :param event: the whois channel event
        :return: None
        """
        self.bot_requires_channel_join = True
        self.log(u"Got WHOIS information. Bot resides in: " + event.arguments[1], 2, ForegroundColors.WHITE)

        channels = event.arguments[1].split(u"#")
        channels.pop(0)

        for channel in channels:
            if not self.joined_channel:
                channel_to_join = u"#" + channel.split(u" ")[0]
                self.log(u"Joining channel " + channel_to_join, 2, ForegroundColors.WHITE)
                connection.join(channel_to_join)  # Join the channel

    def on_join(self, connection, event):
        u"""
        Once the IRCClient successfully joins a channel, the DCC SEND request is sent to the file serving bot

        :param connection: The IRC connection
        :param event: The event that caused this method to be run
        :return: None
        """
        if event.source.startswith(self.nickname):
            self.log(u"Successfully joined channel", 2, ForegroundColors.WHITE)

            # Send a private message to the bot to request the pack file (xdcc send #packnumber)
            if not self.joined_channel:
                self.log(u"Sending XDCC SEND request to " + self.bot, 2, ForegroundColors.WHITE)
                connection.privmsg(self.bot, u"xdcc send #" + unicode(self.pack))
                self.joined_channel = True

    def on_ctcp(self, connection, event):
        u"""
        This initializes the XDCC file download, once the server is ready to send the file.

        :param connection: The IRC connection
        :param event: The event that caused this method to be run
        :return: None
        """
        self.log(u"ON CTCP: " + unicode(event.arguments), 3, ForegroundColors.BLUE)
        # Make Pycharm happy
        if connection is None or event.arguments[0] != u"DCC":
            return

        # Check that the correct type of CTCP message is received
        try:
            payload = event.arguments[1]
        except IndexError:
            return
        # Parse the arguments
        parts = shlex.split(payload)
        if len(parts) > 6:
            self.log(u"Too many arguments: " + unicode(event.arguments), 3)
            return

        if len(parts) == 5:
            command, filename, peer_address, peer_port, size = parts
        else:
            command, filename, peer_address, peer_port, size, dummy = parts

        self.log(u"Starting Download of " + filename, 2, ForegroundColors.LIGHT_BLUE)

        if command != u"SEND":  # Only react on SENDs
            return

        self.progress_struct.single_size = int(size)  # Store the file size in the progress struct

        # Set the file name, but only if it was not set previously
        if not self.filename:
            self.filename = os.path.join(self.destination_directory, os.path.basename(filename))
        else:
            # Add file extension to override-name
            self.filename += u"." + filename.rsplit(u".", 1)[1]

        # Check if the file already exists. If it does, delete it beforehand
        if os.path.exists(self.filename):
            os.remove(self.filename)

        self.file = open(self.filename, u"wb")  # Open the file for writing
        peer_address = irc.client.ip_numstr_to_quad(peer_address)  # Calculate the bot's address
        peer_port = int(peer_port)  # Cast peer port to an integer value
        self.dcc = self.dcc_connect(peer_address, peer_port, u"raw")  # Establish the DCC connection to the bot
        self.log(u"Established DCC connection", 2, ForegroundColors.WHITE)
        self.download_started = True

    def on_dccmsg(self, connection, event):
        u"""
        Run each time a new chunk of data is received while downloading

        :param connection: The IRC connection
        :param event: The event that caused this method to be run
        :return: None
        """
        # Make Pycharm happy
        if connection is None:
            return

        data = event.arguments[0]  # Get the received data
        self.file.write(data)  # and write it to file
        self.progress_struct.single_progress += len(data)  # Increase the progress struct's value

        # Print message to the console once every second
        if self.time_counter < int(time.time()):  # Check the time
            self.time_counter = int(time.time())  # Update the time counter

            # Format the string to print
            single_progress = float(self.progress_struct.single_progress) / float(self.progress_struct.single_size)
            single_progress *= 100.00
            single_progress_formatted_string = u" (%.2f" % single_progress + u" %)"
            progress_fraction = unicode(self.progress_struct.single_progress) + u"/" + unicode(self.progress_struct.single_size)

            # Print, and line return
            if self.verbosity_level > 0:
                print progress_fraction + single_progress_formatted_string,; sys.stdout.write(u"\r")

        # Communicate with the server
        self.dcc.send_bytes(struct.pack(u"!I", self.progress_struct.single_progress))

    def on_dcc_disconnect(self, connection, event):
        u"""
        Whenever the download completes, print a summary to the console and disconnect from the IRC network

        :param connection: The IRC connection
        :param event: The event that caused this method to be run
        :return: None
        """
        # Make Pycharm happy
        if connection is None or event is None:
            pass

        self.file.close()  # Close the file
        # Print a summary of the file
        self.log(u"Received file %s (%d bytes)." % (self.filename, self.progress_struct.single_progress), 1,
                 BackgroundColors.LIGHT_YELLOW)
        self.connection.quit()  # Close the IRC connection

        if self.connection.connected:
            self.on_disconnect(connection, event)

    # noinspection PyMethodMayBeStatic
    def on_disconnect(self, connection, event):
        u"""
        Stop the program when a disconnect occurs (Gets excepted by the start() method)

        :param connection: The IRC connection
        :param event: The event that caused this method to be run
        :return: None
        """
        self.log(u"Disconnected", 2, ForegroundColors.RED)
        # Make Pycharm happy
        if connection is None:
            pass
        if event.arguments[0] == u"Bot does not exist on server":
            raise ConnectionAbortedError(u"Bot does not exist on server")
        if event.arguments[0] == u"TIMEOUT":
            raise ConnectionError(u"Timeout")
        else:
            sys.exit(0)

    def on_privmsg(self, connection, event):
        u"""
        Logs a private message
        :param connection: the IRC connection
        :param event: the message event
        :return: None
        """
        if connection is None:
            pass
        self.log(u"PRIVATE MESSAGE: " + unicode(event.arguments), 4, ForegroundColors.YELLOW)

    def on_privnotice(self, connection, event):
        u"""
        Logs a private notice
        :param connection: the IRC connection
        :param event: the notice event
        :return: None
        """
        if connection is None:
            pass
        self.log(u"PRIVATE NOTICE: " + unicode(event.arguments), 4, ForegroundColors.LIGHT_YELLOW)

    def on_pubmsg(self, connection, event):
        u"""
        Logs a public message
        :param connection: the IRC connection
        :param event: the message event
        :return: None
        """
        if connection is None:
            pass
        self.log(u"PUBLIC MESSAGE: " + unicode(event.arguments), 4, ForegroundColors.MAGENTA)

    def on_pubnotice(self, connection, event):
        u"""
        Logs a public notice
        :param connection: the IRC connection
        :param event: the notice event
        :return: None
        """
        if connection is None:
            pass
        self.log(u"PUBLIC NOTICE: " + unicode(event.arguments), 4, ForegroundColors.LIGHT_MAGENTA)
