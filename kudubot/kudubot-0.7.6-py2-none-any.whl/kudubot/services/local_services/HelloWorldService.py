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


class HelloWorldService(Service):
    u"""
    The HelloWorldService Class that extends the generic Service class.
    It sends a Hello World code snipped in the requested programming language
    """

    identifier = u"hello_world"
    u"""
    The identifier for this service
    """

    help_description = {u"en": u"/helloworld\tSends a message containing how to write a 'Hello World'"
                              u"Program in a specific language\n"
                              u"syntax:\n"
                              u"/helloworld <language|list>",
                        u"de": u"/helloworld\tSchickt eine Nachricht mit einem 'Hello World' Codeschnipsel für eine"
                              u"spezifische Programmiersprache\n"
                              u"syntax:\n"
                              u"/helloworld <sprache|liste>"}
    u"""
    Help description for this service.
    """

    implementations = {u"python": u"print(\"Hello World!\")",
                       u"python2": u"print \"Hello World!\"",
                       u"python3": u"print(\"Hello World!\")",
                       u"java": u"pubic class Main {\n"
                               u"    public static void main(String[] args) {\n"
                               u"        System.out.println(\"Hello World!\");\n"
                               u"    }\n"
                               u"}",
                       u"c": u"#include <stdio.h>\n\n"
                            u"int main() {\n"
                            u"    printf(\"Hello World!\\n\");\n"
                            u"    return 0;\n"
                            u"}",
                       u"c++": u"#include <iostream>\n\n"
                              u"int main() {\n"
                              u"    std::cout << \"Hello World!\";\n"
                              u"    return 0;\n"
                              u"}",
                       u"bash": u"echo \"Hello World\"",
                       u"rust": u"fn main() {\n"
                               u"    println!(\"Hello World!\");\n"
                               u"}",
                       u"ruby": u"puts 'Hello, world!'",
                       u"perl": u"print \"Hello World!\\n\";",
                       u"c#": u"using System;\n"
                             u"namespace HelloWorldApplication{\n"
                             u"    class HelloWorld {\n"
                             u"        Console.WriteLine(\"Hello World!\");\n"
                             u"        Console.ReadKey();\n"
                             u"    }\n"
                             u"}",
                       u"basic": u"10 PRINT \"Hello World!\"",
                       u"visual basic": u"Module HelloWorld\n"
                                       u"    Sub Main()\n"
                                       u"        System.Console.WriteLine(\"Hello World!\")\n"
                                       u"        System.Console.ReadLine()\n"
                                       u"        End\n"
                                       u"    End Sub\n"
                                       u"End Module\n",
                       u"brainfuck": u"++++++++++\n"
                                    u"[\n"
                                    u" >+++++++>++++++++++>+++>+<<<<-\n"
                                    u"]\n"
                                    u">++.\n"
                                    u">+.\n"
                                    u"+++++++.\n"
                                    u".\n"
                                    u"+++.\n"
                                    u">++.\n"
                                    u"<<+++++++++++++++.\n"
                                    u">.\n"
                                    u"+++.\n"
                                    u"------.\n"
                                    u"--------.\n"
                                    u">+.\n"
                                    u">.\n"
                                    u"+++.",
                       u"haskell": u"main = putStrLn \"Hello World!\"",
                       u"erlang": u"-module(hello).\n"
                                 u"-export([hello_world/0]).\n\n"
                                 u"hello_world() -> io:fwrite(\"Hello World!\n\").",
                       u"prolog": u"?- write('Hello World!'), nl.",
                       u"swift": u"print(\"Hello World!\")",
                       u"b": u"main() {\n"
                            u"    printf(\"Hello World!\");\n"
                            u"}",
                       u"d": u"import std.stdio;\n"
                            u"void main() {\n"
                            u"    writeln(\"Hello World!\");\n"
                            u"}",
                       u"cobol": u"000100 IDENTIFICATION DIVISION.\n"
                                u"000200 PROGRAM-ID. HELLOWORLD.\n"
                                u"000900 PROCEDURE DIVISION.\n"
                                u"001000 MAIN.\n"
                                u"001100 DISPLAY \"Hello World!\".\n"
                                u"001200 STOP RUN.",
                       u"fortran": u"program hello\n"
                                  u"write(*,*) \"Hello World!\"\n"
                                  u"end program hello",
                       u"go": u"package main\n\n"
                             u"import \"fmt\"\n\n"
                             u"func main() {\n"
                             u"    fmt.Println(\"Hello World!\")\n"
                             u"}",
                       u"lua": u"print (\"Hello World!\")",
                       u"x86 assembly": u"section .data\n"
                                       u"str:     db 'Hello World!', 0Ah\n"
                                       u"str_len: equ $ - str\n\n\n"
                                       u"section .text\n"
                                       u"global _start\n\n"
                                       u"_start:\n"
                                       u"    mov eax, 4\n"
                                       u"    mov ebx, 1\n\n"
                                       u"    mov ecx, str\n"
                                       u"    mov edx, str_len\n"
                                       u"    int 80h\n\n"
                                       u"    mov eax, 1\n"
                                       u"    mov ebx, 0\n"
                                       u"    int 80h",
                       u"shakespeare": u"Romeo, a young man with a remarkable patience.\n"
                                       u"Juliet, a likewise young woman of remarkable grace.\n"
                                       u"Ophelia, a remarkable woman much in dispute with Hamlet.\n"
                                       u"Hamlet, the flatterer of Andersen Insulting A/S.\n",
                       u"0815": u"<:48:x<:65:=<:6C:$=$=$$~<:03:+\n"
                               u"$~<:ffffffffffffffb1:+$<:77:~$\n"
                               u"~<:fffffffffffff8:x+$~<:03:+$~\n"
                               u"<:06:x-$x<:0e:x-$=x<:43:x-$",
                       u"blub": u"blub. blub? blub. blub. blub. blub. blub. blub. blub. blub. blub. blub. blub. blub. "
                               u"blub. blub. blub. blub. blub. blub. blub! blub?\n"
                               u"blub? blub. blub. blub. blub. blub. blub. blub. blub. blub. blub. blub. blub. blub. "
                               u"blub. blub. blub. blub. blub. blub? blub! blub!\n"
                               u"blub? blub! blub? blub. blub! blub. blub. blub? blub. blub. blub. blub. blub. blub. "
                               u"blub. blub. blub. blub. blub. blub. blub. blub.\n"
                               u"blub! blub? blub? blub. blub. blub. blub. blub. blub. blub. blub. blub. blub. blub? "
                               u"blub! blub! blub? blub! blub? blub. blub. blub.\n"
                               u"blub! blub. blub. blub. blub. blub. blub. blub. blub. blub. blub. blub. blub. blub. "
                               u"blub. blub. blub! blub. blub! blub. blub. blub.\n"
                               u"blub. blub. blub. blub. blub! blub. blub. blub? blub. blub? blub. blub? blub. blub. "
                               u"blub. blub. blub. blub. blub. blub. blub. blub.\n"
                               u"blub. blub. blub. blub. blub. blub. blub! blub? blub? blub. blub. blub. blub. blub. "
                               u"blub. blub. blub. blub. blub. blub? blub! blub!\n"
                               u"blub? blub! blub? blub. blub! blub. blub. blub? blub. blub? blub. blub? blub. blub. "
                               u"blub. blub. blub. blub. blub. blub. blub. blub.\n"
                               u"blub. blub. blub. blub. blub. blub. blub. blub. blub. blub. blub! blub? blub? blub. "
                               u"blub. blub. blub. blub. blub. blub. blub. blub.\n"
                               u"blub. blub. blub. blub. blub. blub. blub. blub. blub. blub. blub. blub? blub! blub! "
                               u"blub? blub! blub? blub. blub! blub! blub! blub!\n"
                               u"blub! blub! blub! blub. blub? blub. blub? blub. blub? blub. blub? blub. blub! blub. "
                               u"blub. blub. blub. blub. blub. blub. blub! blub.\n"
                               u"blub! blub! blub! blub! blub! blub! blub! blub! blub! blub! blub! blub! blub! blub. "
                               u"blub! blub! blub! blub! blub! blub! blub! blub!\n"
                               u"blub! blub! blub! blub! blub! blub! blub! blub! blub! blub. blub. blub? blub. blub?"
                               u"blub. blub. blub! blub."}
    u"""
    The actual implementations of hello world in the different languages
    """

    language_not_found_error = {u"en": u"Programming Language not found",
                                u"de": u"Programmiersprache nicht gefunden"}
    u"""
    Error message sent when the programming language could not be found.
    """

    def process_message(self, message):
        u"""
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        prog_language = message.message_body.lower().split(u" ", 1)[1]
        if prog_language.startswith(u"list"):
            reply = self.list_languages()
        else:
            reply = self.implementations[prog_language]

        reply_message = self.generate_reply_message(message, u"Hello World", reply)

        if self.connection.identifier in [u"whatsapp", u"telegram"] and not prog_language.startswith(u"list"):
            self.send_text_as_image_message(reply_message)
        else:
            self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message):
        u"""
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = u"^/helloworld (list(e)?|" \
                + Service.regex_string_from_dictionary_keys([HelloWorldService.implementations]) + u")$"
        regex = regex.replace(u"+", u"\+")
        return re.search(re.compile(regex), message.message_body.lower())

    def list_languages(self):
        u"""
        Creates a list of implemented languages

        :return: the list of implemented languages
        """
        list_string = u""
        for language in self.implementations:
            list_string += language + u"\n"
        return list_string.rstrip(u"\n")
