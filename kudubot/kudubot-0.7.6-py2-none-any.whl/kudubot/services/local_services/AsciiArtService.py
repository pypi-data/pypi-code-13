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
from __future__ import absolute_import
import re

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message


class AsciiArtService(Service):
    u"""
    The AsciiArtService Class that extends the generic Service class.
    It sends an ASCII Art image.
    """

    identifier = u"ascii_art"
    u"""
    The identifier for this service
    """

    help_description = {u"en": u"/ascii\tSends an image of a specified ASCII art\n"
                              u"syntax:\n"
                              u"/ascii list (Lists all available images)"
                              u"/ascii <image>",
                        u"de": u"/ascii\tSchickt ein Bild mit ASCII Kunst\n"
                              u"syntax:\n"
                              u"/ascii liste (Listet alle verfügbaren bilder auf)"
                              u"/ascii linux ascii art<bild>"}
    u"""
    Help description for this service.
    """

    art = {u"tux": u"         a8888b.\n"
                  u"        d888888b.\n"
                  u"        8P\"YP\"Y88\n"
                  u"        8|o||o|88\n"
                  u"        8'    .88\n"
                  u"        8`._.' Y8.\n"
                  u"       d/      `8b.\n"
                  u"     .dP   .     Y8b.\n"
                  u"    d8:'   \"   `::88b.\n"
                  u"   d8\"           `Y88b\n"
                  u"  :8P     '       :888\n"
                  u"   8a.    :      _a88P\n"
                  u" ._/\"Yaa_ :    .| 88P|\n"
                  u" \    YP\"      `| 8P  `.\n"
                  u" /     \._____.d|    .'\n"
                  u" `--..__)888888P`._.'\n",
           u"bigtux": u"                         ooMMMMMMMooo\n"
                     u"                       oMMMMMMMMMMMMMMMoo\n"
                     u"                      MMMMMMMMMMMMMMo\"MMMo\n"
                     u"                     \"MMMMMMMMMMMMMMMMMMMMM\n"
                     u"                     MMMMMMMMMMMMMMMMMMMMMMo\n"
                     u"                     MMMM\"\"MMMMMM\"o\" MMMMMMM\n"
                     u"                     MMo o\" MMM\"  oo \"\"MMMMM\n"
                     u"                     MM MMo MMM\" MMoM \"MMMMM\n"
                     u"                     MMo\"M\"o\" \"\" MMM\" oMMMMM\"\n"
                     u"                     oMM M  o\" \" o \"o MMMMMM\"\n"
                     u"                     oM\"o \" o \"  o \"o MMMMMMM\n"
                     u"                     oMMoM o \" M M \"o MMMM\"MMo\n"
                     u"                      Mo \" M \"M \"o\" o  MMMoMMMo\n"
                     u"                     MMo \" \"\" M \"       MMMMMMMo\n"
                     u"                   oMM\"   \"o o \"         MMMMMMMM\n"
                     u"                  MMM\"                    MMMMMMMMo\n"
                     u"                oMMMo                     \"MMMMMMMMo\n"
                     u"               MMMMM o             \"  \" o\" \"MMMMMMMMMo\n"
                     u"              MMMMM          \"            \" \"MMMMMMMMMo\n"
                     u"             oMMMM                          \"\"MMMMMMMMMo\n"
                     u"            oMMMM         o         o         MMoMMMMMMM\n"
                     u"            MMMM               o              \"MMMMMMMMMM\n"
                     u"           MMMM\"     o    o             o     \"MMMMMMMMMMo\n"
                     u"         oMMMMM                                MMMMMMMMMMo\n"
                     u"         MMM\"MM                               \"MMM\"MMMMMMM\n"
                     u"         MMMMMM           \"      o   \"         MMMMMMMMMMM\n"
                     u"         \"o  \"ooo    o                     o o\"MMMMMMMMoM\"\n"
                     u"        \" o \"o \"MMo       \"                o\"  MMMMMMMM\"\n"
                     u"    o \"o\" o o \"  MMMo                     o o\"\"\"\"MMMM\"o\" \"\n"
                     u" \" o \"o \" o o\" \"  MMMMoo         \"       o \"o M\"\" M \"o \" \"\n"
                     u" \"o o\"  \" o o\" \" \" \"MMMM\"   o              M o \"o\" o\" o\" \" o\n"
                     u" M  o M \"  o \" \" \" \" MM\"\"           o    oMo\"o \" o o \"o \" \"o \"\n"
                     u" o\"  o \" \"o \" \" M \" \" o                MMMMo\"o \" o o o o\" o o\" \"\n"
                     u" o\" \"o \" o \" \" o o\" M \"oo         ooMMMMMMM o \"o o o \" o o o \"\n"
                     u" M \"o o\" o\" \"o o o \" o\"oMMMMMMMMMMMMMMMMMMMo\" o o \"o \"o o\"\n"
                     u"  \"\" \"o\"o\"o\"o o\"o \"o\"o\"oMMMMMMMMMMMMMMMMMMo\"o\"o \"o o\"oo\"\n"
                     u"        \"\" M Mo\"o\"oo\"oM\"\" \"               MMoM M M M\n"
                     u"               \"\"\" \"\"\"                      \" \"\"\" \"\n",
           u"elephant": u"              ___.-~\"~-._   __....__\n"
                       u"            .'    `    \\ ~\"~        ``-.\n"
                       u"           /` _      )  `\\              `\\\n"
                       u"          /`  a)    /     |               `\\\n"
                       u"         :`        /      |                 \\\n"
                       u"    <`-._|`  .-.  (      /   .            `;\\\\\n"
                       u"     `-. `--'_.'-.;\\___/'   .      .       | \\\\\n"
                       u"  _     /:--`     |        /     /        .'  \\\\\n"
                       u" (\"\\   /`/        |       '     '         /    :`;\n"
                       u" `\\'\\_/`/         .\\     /`~`=-.:        /     ``\n"
                       u"   `._.'          /`\\    |      `\\      /(\n"
                       u"                 /  /\\   |        `Y   /  \\\n"
                       u"                J  /  Y  |         |  /`\\  \\\n"
                       u"               /  |   |  |         |  |  |  |\n"
                       u"              \"---\"  /___|        /___|  /__|\n"
                       u"                     '\"\"\"         '\"\"\"  '\"\"\"\n",
           u"snake_flute": u"      ,'._,`.\n"
                          u"     (-.___.-)\n"
                          u"     (-.___.-)\n"
                          u"     `-.___.-'                  \n"
                          u"      ((  @ @|              .            __\n"
                          u"       \\   ` |         ,\\   |`.    @|   |  |      _.-._\n"
                          u"      __`.`=-=mm===mm:: |   | |`.   |   |  |    ,'=` '=`.\n"
                          u"     (    `-'|:/  /:/  `/  @| | |   |, @| @|   /---)W(---\\\n"
                          u"      \\ \\   / /  / /         @| |   '         (----| |----) ,~\n"
                          u"      |\\ \\ / /| / /            @|              \\---| |---/  |\n"
                          u"      | \\ V /||/ /                              `.-| |-,'   |\n"
                          u"      |  `-' |V /                                 \\| |/    @'\n"
                          u"      |    , |-'                                 __| |__\n"
                          u"      |    .;: _,-.                         ,--\"\"..| |..\"\"--.\n"
                          u"      ;;:::' \"    )                        (`--::__|_|__::--')\n"
                          u"    ,-\"      _,  /                          \\`--...___...--'/   \n"
                          u"   (    -:--'/  /                           /`--...___...--'\\\n"
                          u"    \"-._  `\"'._/                           /`---...___...---'\\\n"
                          u"        \"-._   \"---.                      (`---....___....---')\n"
                          u"         .' \",._ ,' )                     |`---....___....---'|\n"
                          u"         /`._|  `|  |                     (`---....___....---') \n"
                          u"        (   \\    |  /                      \\`---...___...---'/\n"
                          u"         `.  `,  ^\"\"                        `:--...___...--;'\n"
                          u"           `.,'                               `-._______.-'\n"
           }

    def process_message(self, message):
        u"""
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        image_to_show = message.message_body.lower().split(u" ", 1)[1]
        if image_to_show.startswith(u"list"):
            reply = self.list_images()
        else:
            reply = self.art[image_to_show]

        reply_message = self.generate_reply_message(message, u"ASCII Art", reply)

        if self.connection.identifier in [u"whatsapp", u"telegram"] and not image_to_show.startswith(u"list"):
            self.send_text_as_image_message(reply_message)
        else:
            self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message):
        u"""
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = u"^/ascii (list(e)?|" \
                + Service.regex_string_from_dictionary_keys([AsciiArtService.art]) + u")$"
        regex = regex.replace(u"+", u"\+")
        return re.search(re.compile(regex), message.message_body.lower())

    def list_images(self):
        u"""
        Creates a list of implemented images

        :return: the list of implemented images
        """
        list_string = u""
        for image in self.art:
            list_string += image + u"\n"
        return list_string.rstrip(u"\n")
