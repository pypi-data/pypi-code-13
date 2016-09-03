# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

longdesc = '''tgcode
======

| *tgcode* is a simple library that let's you convert binary data into a
  string and vice-versa.
| This could be useful for sharing files via an IRC channel, send files
  via pastebin like services, make you own protocol that uses this
  library or anything like that.

Installation
============

You can install using the ``pip`` command line utility.

::

    pip install tgcode

Usage
=====

It's simple, just use the ``encode()`` and ``decode()`` functions, just
like that:

.. code:: python

    import tgcode

    data = b'Hello, World!'

    encoded = tgcode.encode(data)

    decoded = tgcode.decode(encoded)

    print('Are they equals: {}'.format(decoded==data))

Complex Usage
=============

| Okay, okay, you want more information that a snippet? Here we go:

encode()
--------
 
|  The ``encode()`` encodes a binary value into a decodable
  string. It receives as argument the ``bytes()`` that will be encoded
  and returns the encoded ``str()``
| Example:

.. code:: python

    import tgcode

    data = b'Hello, World!' #bytes data to be encoded

    encoded_data = tgcode.encode(data) #encodes the data

    print('Encoded bytes: {}'.format(encoded_data)) #prints the encoded data

decode()
--------

| The ``decode()`` function accepts as argument a string returned by
  ``decode()`` or ``fast_decode()``. It receives as argument the
  ``str()`` that will be decoded and returns the decoded ``bytes()``.
| Example:

.. code:: python

    import tgcode

    encoded_data = '_=}o§}v§}v§}y=SG}=}y§}B§}v§}n=H' #the encoded string

    data = tgcode.decode(encoded_data) #decodes the string

    file = open('tgcode.test', 'wb') #opens a file with "write binary" flag

    file.write(data) #writes the decoded data into the file

    file.close() #saves the file

fast\_encode()
--------------

| This function splits the data and encodes him in different threads.
  The arguments are exactly equals to the ``encode()``'s arguments,
  except for the extra ``thread_quantity`` argument, that are an integer
  (``int()``) with the amount of threads that will be used. **JUST** use
  this function for binaries biggest than the number of threads, like
  files or big messages. The default ``thread_quantity`` value are 35.
| Example:

.. code:: python

    import tgcode

    file = open('tgcode.test', 'rb') #opens the file with "read binary" flag

    data = file.read() #reads the data

    fast_encoded = tgcode.fast_encode(data) #fastly encodes the data

    file.close() #closes the file

    print('Fastly encoded data: {}'.format(fast_encoded)) #prints the encoded data

License
=======

MIT license 

.. code::

    Copyright (c) 2016

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the
    "Software"), to deal in the Software without restriction, including
    without limitation the rights to use, copy, modify, merge, publish,
    distribute, sublicense, and/or sell copies of the Software, and to
    permit persons to whom the Software is furnished to do so, subject to
    the following conditions:

    The above copyright notice and this permission notice shall be included
    in all copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
    OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
    CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. \`\`\`notice and
    this permission notice shall be included in all copies or substantial
    portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
    OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
    CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Author
======
| The author of this tool wants to be called as "thegamerbr1". In
 case of bugs, ideas or help, contact: 
| - Skype: xthegamerbr1x
| Telegram: @thegamerbr1 
| - Email (slow response): xthegamerbr1x@gmail.com
'''

setup(
    name = "TGCode",
    version = "0.3.0.post2",
    packages = find_packages(),
    author = "thegamerbr1",
    author_email = "xthegamerbr1x@gmail.com",
    description = "TGCode is a simple library that let's you convert binary data into a string and vice-versa.",
    license = "MIT",
    long_description = longdesc,
    keywords = "encoding binary bytes string data irc file bin convert ",
)