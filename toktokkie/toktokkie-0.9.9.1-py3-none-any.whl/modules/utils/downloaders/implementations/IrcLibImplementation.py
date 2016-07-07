"""
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
import os
import random
import shlex
import struct
import sys
import time
import irc.client
from toktokkie.modules.objects.ProgressStruct import ProgressStruct


class IrcLibImplementation(irc.client.SimpleIRCClient):
    """
    This class extends the SimpleIRCClient Class to download XDCC packs using the irclib library
    It is based on the tutorial scripts on the library's Github page, but strongly modified to suit the
    needs of the batch download manager.
    """

    server = ""
    """
    The server address of the server the downloader has to connect to.
    """

    bot = ""
    """
    The bot serving the requested file
    """

    pack = -1
    """
    The pack number of the file to be downloaded
    """

    destination_directory = ""
    """
    The directory to which the file should be downloaded to
    """

    nickname = ""
    """
    A nickname for the bot
    """

    progress_struct = None
    """
    A progress struct to share the download progress between threads
    """

    filename = ""
    """
    The path to the downloaded file
    """

    file = None
    """
    The downloaded file opened for writing
    """

    dcc = None
    """
    The established DCC connection to the file server bot
    """

    time_counter = int(time.time())
    """
    Keeps track of the time to control how often status updates about the download are printed to the console
    """

    common_servers = ["irc.rizon.net", "irc.criten.net", "irc.scenep2p.net", "irc.freenode.net", "irc.abjects.net"]
    """
    A list of common servers to try in case a bot does not exist on a server
    """

    server_retry_counter = 0
    """
    Counter for server retries
    """

    verbose = False
    """
    Variable to determine the verbosity of the input
    """

    def __init__(self, server: str, bot: str, pack: int, destination_directory: str, progress_struct: ProgressStruct,
                 file_name_override: str = None, verbose: bool = False) -> None:
        """
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
        super().__init__()

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

    def log(self, string: str) -> None:
        """
        Prints a string, if the verbose option is set

        :param string: the string to print
        :return: None
        """
        if self.verbose:
            print(string)

    def connect(self) -> None:
        """
        Connects to the server with a randomly generated username
        :return: None
        """
        self.nickname = "media_manager_python" + str(random.randint(0, 1000000))  # Generate random nickname
        self.log("Connecting to server " + self.server + " at port 6667 as user " + self.nickname)
        super().connect(self.server, 6667, self.nickname)  # Connect to server

    def start(self) -> str:
        """
        Starts the download process and returns the file path of the downloaded file once the download completes
        :return: the path to the downloaded file
        """
        self.log("Starting Download")
        download_started = False
        while not download_started:
            download_started = True
            try:
                self.connect()  # Connect to server
                super().start()  # Start the download

            except (UnicodeDecodeError, irc.client.ServerConnectionError):
                download_started = False
                if os.path.isfile(self.filename):
                    os.remove(self.filename)
                self.log("Download failed, retrying...")

            except ConnectionAbortedError:
                try:
                    self.server = self.common_servers[self.server_retry_counter]
                    self.server_retry_counter += 1
                    download_started = False
                    self.log("Trying different server...")
                except IndexError:
                    raise ConnectionError("Failed to find the bot on any known server")

            except (SystemExit, ConnectionError):
                pass  # If disconnect occurs, catch and ignore the system exit call

            if not self.progress_struct.single_progress == self.progress_struct.single_size:
                self.log("Download not completed successfully, trying again")
                download_started = False
                if os.path.isfile(self.filename):
                    os.remove(self.filename)

        return self.filename  # Return the file path

    def on_welcome(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Method run when the IRCClient successfully connects to a server. It sends a whois request
        to find out which channel to join

        :param connection: The IRC connection
        :param event: The event that caused this method to be run
        :return: None
        """
        # Make Pycharm happy
        if event is None:
            return
        self.log("Connection to server " + self.server + " established. Sending WHOIS command for " + self.bot)
        connection.whois(self.bot)

    def on_nosuchnick(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Checks if there exists a bot with the specified name on the server

        :param connection: the IRC connection
        :param event: the nosuchnick event
        :return: None
        """
        self.log("NOSUCHNICK")
        if connection is None:
            pass
        if event.arguments[0] == self.bot:
            connection.disconnect("Bot does not exist on server")

    # noinspection PyMethodMayBeStatic
    def on_whoischannels(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Checks the channels the bot is connected to.

        :param connection: the IRC connection
        :param event: the whois channel event
        :return: None
        """
        self.log("Got WHOIS information. Bot resides in: " + event.arguments[1])
        channel_to_join = event.arguments[1].split("%")[1].split(" ")[0]
        self.log("Joining channel " + channel_to_join)
        connection.join(channel_to_join)  # Join the channel

    def on_join(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Once the IRCClient successfully joins a channel, the DCC SEND request is sent to the file serving bot

        :param connection: The IRC connection
        :param event: The event that caused this method to be run
        :return: None
        """
        if event.source.startswith(self.nickname):
            self.log("Successfully joined channel")
            self.log("Sending XDCC SEND request to " + self.bot)
            # Send a private message to the bot to request the pack file (xdcc send #packnumber)
            connection.privmsg(self.bot, "xdcc send #" + str(self.pack))

    def on_ctcp(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
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
            self.log("Too many arguments: " + str(event.arguments))
            return
        command, filename, peer_address, peer_port, size = parts
        if command != "SEND":  # Only react on SENDs
            return

        self.progress_struct.single_size = int(size)  # Store the file size in the progress struct

        # Set the file name, but only if it was not set previously
        if not self.filename:
            self.filename = os.path.join(self.destination_directory, os.path.basename(filename))
        else:
            # Add file extension to override-name
            self.filename += "." + filename.rsplit(".", 1)[1]

        # Check if the file already exists. If it does, delete it beforehand
        if os.path.exists(self.filename):
            os.remove(self.filename)

        self.file = open(self.filename, "wb")  # Open the file for writing
        peer_address = irc.client.ip_numstr_to_quad(peer_address)  # Calculate the bot's address
        peer_port = int(peer_port)  # Cast peer port to an integer value
        self.dcc = self.dcc_connect(peer_address, peer_port, "raw")  # Establish the DCC connection to the bot
        self.log("Established DCC connection")

    def on_dccmsg(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
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
            single_progress_formatted_string = " (%.2f" % single_progress + " %)"
            progress_fraction = str(self.progress_struct.single_progress) + "/" + str(self.progress_struct.single_size)

            # Print, and line return
            print(progress_fraction + single_progress_formatted_string, end="\r")

        # Communicate with the server
        self.dcc.send_bytes(struct.pack("!I", self.progress_struct.single_progress))

    def on_dcc_disconnect(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
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
        print("Received file %s (%d bytes)." % (self.filename,
                                                self.progress_struct.single_progress))
        self.connection.quit()  # Close the IRC connection

        if self.connection.connected:
            self.on_disconnect(connection, event)

    # noinspection PyMethodMayBeStatic
    def on_disconnect(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Stop the program when a disconnect occurs (Gets excepted by the start() method)

        :param connection: The IRC connection
        :param event: The event that caused this method to be run
        :return: None
        """
        self.log("Disconnected")
        # Make Pycharm happy
        if connection is None:
            pass
        if event.arguments[0] == "Bot does not exist on server":
            raise ConnectionAbortedError("Bot does not exist on server")
        else:
            sys.exit(0)

    def on_privmsg(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Logs a private message
        :param connection: the IRC connection
        :param event: the message event
        :return: None
        """
        if connection is None:
            pass
        self.log("PRIVATE MESSAGE: " + str(event.arguments))

    def on_privnotice(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Logs a private notice
        :param connection: the IRC connection
        :param event: the notice event
        :return: None
        """
        if connection is None:
            pass
        self.log("PRIVATE NOTICE: " + str(event.arguments))

    def on_pubmsg(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Logs a public message
        :param connection: the IRC connection
        :param event: the message event
        :return: None
        """
        if connection is None:
            pass
        self.log("PUBLIC MESSAGE: " + str(event.arguments))

    def on_pubnotice(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Logs a public notice
        :param connection: the IRC connection
        :param event: the notice event
        :return: None
        """
        if connection is None:
            pass
        self.log("PUBLIC NOTICE: " + str(event.arguments))
