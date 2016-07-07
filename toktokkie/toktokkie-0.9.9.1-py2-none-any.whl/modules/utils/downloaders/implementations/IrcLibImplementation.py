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
from toktokkie.modules.objects.ProgressStruct import ProgressStruct
from io import open


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

    verbose = False
    u"""
    Variable to determine the verbosity of the input
    """

    def __init__(self, server, bot, pack, destination_directory, progress_struct,
                 file_name_override = None, verbose = False):
        u"""
        Constructor for the IrcLibImplementation class. It initializes the base SimpleIRCClient class
        and stores the necessary information for the download process as class variables

        :param server: The server to which the Downloader needs to connect to
        :param bot: The bot serving the file to download
        :param pack: The pack number of the file to download
        :param destination_directory: The destination directory of the downloaded file
        :param progress_struct: The progress struct to keep track of the download progress between threads
        :param file_name_override: Can be set to pre-determine the file name of the downloaded file
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
        self.verbose = verbose

        # Remove the server from common server list if it is included there
        try:
            self.common_servers.remove(server)
        except ValueError:
            pass

        # If a file name is pre-defined, set the file name to be that name.
        if file_name_override is not None:
            self.filename = os.path.join(destination_directory, file_name_override)

    def log(self, string):
        u"""
        Prints a string, if the verbose option is set

        :param string: the string to print
        :return: None
        """
        if self.verbose:
            print string

    def connect(self):
        u"""
        Connects to the server with a randomly generated username
        :return: None
        """
        self.nickname = u"media_manager_python" + unicode(random.randint(0, 1000000))  # Generate random nickname
        self.log(u"Connecting to server " + self.server + u" at port 6667 as user " + self.nickname)
        super(IrcLibImplementation, self).connect(self.server, 6667, self.nickname)  # Connect to server

    def start(self):
        u"""
        Starts the download process and returns the file path of the downloaded file once the download completes
        :return: the path to the downloaded file
        """
        self.log(u"Starting Download")
        download_started = False
        while not download_started:
            download_started = True
            try:
                self.connect()  # Connect to server
                super(IrcLibImplementation, self).start()  # Start the download

            except (UnicodeDecodeError, irc.client.ServerConnectionError):
                download_started = False
                if os.path.isfile(self.filename):
                    os.remove(self.filename)
                self.log(u"Download failed, retrying...")

            except ConnectionAbortedError:
                try:
                    self.server = self.common_servers[self.server_retry_counter]
                    self.server_retry_counter += 1
                    download_started = False
                    self.log(u"Trying different server...")
                except IndexError:
                    raise ConnectionError(u"Failed to find the bot on any known server")

            except (SystemExit, ConnectionError):
                pass  # If disconnect occurs, catch and ignore the system exit call

            if not self.progress_struct.single_progress == self.progress_struct.single_size:
                self.log(u"Download not completed successfully, trying again")
                download_started = False
                if os.path.isfile(self.filename):
                    os.remove(self.filename)

        return self.filename  # Return the file path

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
        self.log(u"Connection to server " + self.server + u" established. Sending WHOIS command for " + self.bot)
        connection.whois(self.bot)

    def on_nosuchnick(self, connection, event):
        u"""
        Checks if there exists a bot with the specified name on the server

        :param connection: the IRC connection
        :param event: the nosuchnick event
        :return: None
        """
        self.log(u"NOSUCHNICK")
        if connection is None:
            pass
        if event.arguments[0] == self.bot:
            connection.disconnect(u"Bot does not exist on server")

    # noinspection PyMethodMayBeStatic
    def on_whoischannels(self, connection, event):
        u"""
        Checks the channels the bot is connected to.

        :param connection: the IRC connection
        :param event: the whois channel event
        :return: None
        """
        self.log(u"Got WHOIS information. Bot resides in: " + event.arguments[1])
        channel_to_join = event.arguments[1].split(u"%")[1].split(u" ")[0]
        self.log(u"Joining channel " + channel_to_join)
        connection.join(channel_to_join)  # Join the channel

    def on_join(self, connection, event):
        u"""
        Once the IRCClient successfully joins a channel, the DCC SEND request is sent to the file serving bot

        :param connection: The IRC connection
        :param event: The event that caused this method to be run
        :return: None
        """
        if event.source.startswith(self.nickname):
            self.log(u"Successfully joined channel")
            self.log(u"Sending XDCC SEND request to " + self.bot)
            # Send a private message to the bot to request the pack file (xdcc send #packnumber)
            connection.privmsg(self.bot, u"xdcc send #" + unicode(self.pack))

    def on_ctcp(self, connection, event):
        u"""
        This initializes the XDCC file download, once the server is ready to send the file.

        :param connection: The IRC connection
        :param event: The event that caused this method to be run
        :return: None
        """
        self.log(event.arguments)
        # Make Pycharm happy
        if connection is None:
            return

        # Check that the correct type of CTCP message is received
        try:
            payload = event.arguments[1]
        except IndexError:
            return
        # Parse the arguments
        parts = shlex.split(payload)
        if len(parts) != 5:
            self.log(u"Too many arguments: " + unicode(event.arguments))
            return
        command, filename, peer_address, peer_port, size = parts
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
        self.log(u"Established DCC connection")

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
        print u"Received file %s (%d bytes)." % (self.filename,
                                                self.progress_struct.single_progress)
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
        self.log(u"Disconnected")
        # Make Pycharm happy
        if connection is None:
            pass
        if event.arguments[0] == u"Bot does not exist on server":
            raise ConnectionAbortedError(u"Bot does not exist on server")
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
        self.log(u"PRIVATE MESSAGE: " + unicode(event.arguments))

    def on_privnotice(self, connection, event):
        u"""
        Logs a private notice
        :param connection: the IRC connection
        :param event: the notice event
        :return: None
        """
        if connection is None:
            pass
        self.log(u"PRIVATE NOTICE: " + unicode(event.arguments))

    def on_pubmsg(self, connection, event):
        u"""
        Logs a public message
        :param connection: the IRC connection
        :param event: the message event
        :return: None
        """
        if connection is None:
            pass
        self.log(u"PUBLIC MESSAGE: " + unicode(event.arguments))

    def on_pubnotice(self, connection, event):
        u"""
        Logs a public notice
        :param connection: the IRC connection
        :param event: the notice event
        :return: None
        """
        if connection is None:
            pass
        self.log(u"PUBLIC NOTICE: " + unicode(event.arguments))
