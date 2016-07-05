# -*- coding: utf-8 -*-

# Copyright (C) 2005  Michael Urman
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of version 2 of the GNU General Public License as
# published by the Free Software Foundation.

import zlib
from struct import unpack

from ._util import ID3JunkFrameError, ID3EncryptionUnsupportedError, unsynch
from ._specs import (
    BinaryDataSpec, StringSpec, Latin1TextSpec, EncodedTextSpec, ByteSpec,
    EncodingSpec, ASPIIndexSpec, SizedIntegerSpec, IntegerSpec,
    VolumeAdjustmentsSpec, VolumePeakSpec, VolumeAdjustmentSpec,
    ChannelSpec, MultiSpec, SynchronizedTextSpec, KeyEventSpec, TimeStampSpec,
    EncodedNumericPartTextSpec, EncodedNumericTextSpec, SpecError,
    PictureTypeSpec)
from .._compat import text_type, string_types, swap_to_string, iteritems, izip


def is_valid_frame_id(frame_id):
    return frame_id.isalnum() and frame_id.isupper()


def _bytes2key(b):
    assert isinstance(b, bytes)

    return b.decode("latin1")


class Frame(object):
    """Fundamental unit of ID3 data.

    ID3 tags are split into frames. Each frame has a potentially
    different structure, and so this base class is not very featureful.
    """

    FLAG23_ALTERTAG = 0x8000
    FLAG23_ALTERFILE = 0x4000
    FLAG23_READONLY = 0x2000
    FLAG23_COMPRESS = 0x0080
    FLAG23_ENCRYPT = 0x0040
    FLAG23_GROUP = 0x0020

    FLAG24_ALTERTAG = 0x4000
    FLAG24_ALTERFILE = 0x2000
    FLAG24_READONLY = 0x1000
    FLAG24_GROUPID = 0x0040
    FLAG24_COMPRESS = 0x0008
    FLAG24_ENCRYPT = 0x0004
    FLAG24_UNSYNCH = 0x0002
    FLAG24_DATALEN = 0x0001

    _framespec = []

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and \
                isinstance(args[0], type(self)):
            other = args[0]
            # ask the sub class to fill in our data
            other._to_other(self)
        else:
            for checker, val in izip(self._framespec, args):
                setattr(self, checker.name, val)
            for checker in self._framespec[len(args):]:
                setattr(self, checker.name, kwargs.get(checker.name))

    def __setattr__(self, name, value):
        for checker in self._framespec:
            if checker.name == name:
                self.__dict__[name] = checker.validate(self, value)
                return
        super(Frame, self).__setattr__(name, value)

    def _to_other(self, other):
        # this impl covers subclasses with the same framespec
        if other._framespec is not self._framespec:
            raise ValueError

        for checker in other._framespec:
            setattr(other, checker.name, getattr(self, checker.name))

    def _get_v23_frame(self, **kwargs):
        """Returns a frame copy which is suitable for writing into a v2.3 tag.

        kwargs get passed to the specs.
        """

        new_kwargs = {}
        for checker in self._framespec:
            name = checker.name
            value = getattr(self, name)
            new_kwargs[name] = checker._validate23(self, value, **kwargs)
        return type(self)(**new_kwargs)

    @property
    def HashKey(self):
        """An internal key used to ensure frame uniqueness in a tag"""

        return self.FrameID

    @property
    def FrameID(self):
        """ID3v2 three or four character frame ID"""

        return type(self).__name__

    def __repr__(self):
        """Python representation of a frame.

        The string returned is a valid Python expression to construct
        a copy of this frame.
        """
        kw = []
        for attr in self._framespec:
            # so repr works during __init__
            if hasattr(self, attr.name):
                kw.append('%s=%r' % (attr.name, getattr(self, attr.name)))
        return '%s(%s)' % (type(self).__name__, ', '.join(kw))

    def _readData(self, data):
        """Raises ID3JunkFrameError; Returns leftover data"""

        for reader in self._framespec:
            if len(data):
                try:
                    value, data = reader.read(self, data)
                except SpecError as e:
                    raise ID3JunkFrameError(e)
            else:
                raise ID3JunkFrameError("no data left")
            setattr(self, reader.name, value)

        return data

    def _writeData(self):
        data = []
        for writer in self._framespec:
            data.append(writer.write(self, getattr(self, writer.name)))
        return b''.join(data)

    def pprint(self):
        """Return a human-readable representation of the frame."""
        return "%s=%s" % (type(self).__name__, self._pprint())

    def _pprint(self):
        return "[unrepresentable data]"

    @classmethod
    def _fromData(cls, id3, tflags, data):
        """Construct this ID3 frame from raw string data.

        Raises:

        ID3JunkFrameError in case parsing failed
        NotImplementedError in case parsing isn't implemented
        ID3EncryptionUnsupportedError in case the frame is encrypted.
        """

        if id3.version >= id3._V24:
            if tflags & (Frame.FLAG24_COMPRESS | Frame.FLAG24_DATALEN):
                # The data length int is syncsafe in 2.4 (but not 2.3).
                # However, we don't actually need the data length int,
                # except to work around a QL 0.12 bug, and in that case
                # all we need are the raw bytes.
                datalen_bytes = data[:4]
                data = data[4:]
            if tflags & Frame.FLAG24_UNSYNCH or id3.f_unsynch:
                try:
                    data = unsynch.decode(data)
                except ValueError:
                    # Some things write synch-unsafe data with either the frame
                    # or global unsynch flag set. Try to load them as is.
                    # https://github.com/quodlibet/mutagen/issues/210
                    # https://github.com/quodlibet/mutagen/issues/223
                    pass
            if tflags & Frame.FLAG24_ENCRYPT:
                raise ID3EncryptionUnsupportedError
            if tflags & Frame.FLAG24_COMPRESS:
                try:
                    data = zlib.decompress(data)
                except zlib.error as err:
                    # the initial mutagen that went out with QL 0.12 did not
                    # write the 4 bytes of uncompressed size. Compensate.
                    data = datalen_bytes + data
                    try:
                        data = zlib.decompress(data)
                    except zlib.error as err:
                        raise ID3JunkFrameError(
                            'zlib: %s: %r' % (err, data))

        elif id3.version >= id3._V23:
            if tflags & Frame.FLAG23_COMPRESS:
                usize, = unpack('>L', data[:4])
                data = data[4:]
            if tflags & Frame.FLAG23_ENCRYPT:
                raise ID3EncryptionUnsupportedError
            if tflags & Frame.FLAG23_COMPRESS:
                try:
                    data = zlib.decompress(data)
                except zlib.error as err:
                    raise ID3JunkFrameError('zlib: %s: %r' % (err, data))

        frame = cls()
        frame._readData(data)
        return frame

    def __hash__(self):
        raise TypeError("Frame objects are unhashable")


class FrameOpt(Frame):
    """A frame with optional parts.

    Some ID3 frames have optional data; this class extends Frame to
    provide support for those parts.
    """

    _optionalspec = []

    def __init__(self, *args, **kwargs):
        super(FrameOpt, self).__init__(*args, **kwargs)
        for spec in self._optionalspec:
            if spec.name in kwargs:
                setattr(self, spec.name, kwargs[spec.name])
            else:
                break

    def __setattr__(self, name, value):
        for checker in self._optionalspec:
            if checker.name == name:
                self.__dict__[name] = checker.validate(self, value)
                return
        super(FrameOpt, self).__setattr__(name, value)

    def _to_other(self, other):
        super(FrameOpt, self)._to_other(other)

        # this impl covers subclasses with the same optionalspec
        if other._optionalspec is not self._optionalspec:
            raise ValueError

        for checker in other._optionalspec:
            if hasattr(self, checker.name):
                setattr(other, checker.name, getattr(self, checker.name))

    def _readData(self, data):
        """Raises ID3JunkFrameError; Returns leftover data"""

        for reader in self._framespec:
            if len(data):
                try:
                    value, data = reader.read(self, data)
                except SpecError as e:
                    raise ID3JunkFrameError(e)
            else:
                raise ID3JunkFrameError("no data left")
            setattr(self, reader.name, value)

        if data:
            for reader in self._optionalspec:
                if len(data):
                    try:
                        value, data = reader.read(self, data)
                    except SpecError as e:
                        raise ID3JunkFrameError(e)
                else:
                    break
                setattr(self, reader.name, value)

        return data

    def _writeData(self):
        data = []
        for writer in self._framespec:
            data.append(writer.write(self, getattr(self, writer.name)))
        for writer in self._optionalspec:
            try:
                data.append(writer.write(self, getattr(self, writer.name)))
            except AttributeError:
                break
        return b''.join(data)

    def __repr__(self):
        kw = []
        for attr in self._framespec:
            kw.append('%s=%r' % (attr.name, getattr(self, attr.name)))
        for attr in self._optionalspec:
            if hasattr(self, attr.name):
                kw.append('%s=%r' % (attr.name, getattr(self, attr.name)))
        return '%s(%s)' % (type(self).__name__, ', '.join(kw))


@swap_to_string
class TextFrame(Frame):
    """Text strings.

    Text frames support casts to unicode or str objects, as well as
    list-like indexing, extend, and append.

    Iterating over a TextFrame iterates over its strings, not its
    characters.

    Text frames have a 'text' attribute which is the list of strings,
    and an 'encoding' attribute; 0 for ISO-8859 1, 1 UTF-16, 2 for
    UTF-16BE, and 3 for UTF-8. If you don't want to worry about
    encodings, just set it to 3.
    """

    _framespec = [
        EncodingSpec('encoding'),
        MultiSpec('text', EncodedTextSpec('text'), sep=u'\u0000'),
    ]

    def __bytes__(self):
        return text_type(self).encode('utf-8')

    def __str__(self):
        return u'\u0000'.join(self.text)

    def __eq__(self, other):
        if isinstance(other, bytes):
            return bytes(self) == other
        elif isinstance(other, text_type):
            return text_type(self) == other
        return self.text == other

    __hash__ = Frame.__hash__

    def __getitem__(self, item):
        return self.text[item]

    def __iter__(self):
        return iter(self.text)

    def append(self, value):
        """Append a string."""

        return self.text.append(value)

    def extend(self, value):
        """Extend the list by appending all strings from the given list."""

        return self.text.extend(value)

    def _pprint(self):
        return " / ".join(self.text)


class NumericTextFrame(TextFrame):
    """Numerical text strings.

    The numeric value of these frames can be gotten with unary plus, e.g.::

        frame = TLEN('12345')
        length = +frame
    """

    _framespec = [
        EncodingSpec('encoding'),
        MultiSpec('text', EncodedNumericTextSpec('text'), sep=u'\u0000'),
    ]

    def __pos__(self):
        """Return the numerical value of the string."""
        return int(self.text[0])


class NumericPartTextFrame(TextFrame):
    """Multivalue numerical text strings.

    These strings indicate 'part (e.g. track) X of Y', and unary plus
    returns the first value::

        frame = TRCK('4/15')
        track = +frame # track == 4
    """

    _framespec = [
        EncodingSpec('encoding'),
        MultiSpec('text', EncodedNumericPartTextSpec('text'), sep=u'\u0000'),
    ]

    def __pos__(self):
        return int(self.text[0].split("/")[0])


@swap_to_string
class TimeStampTextFrame(TextFrame):
    """A list of time stamps.

    The 'text' attribute in this frame is a list of ID3TimeStamp
    objects, not a list of strings.
    """

    _framespec = [
        EncodingSpec('encoding'),
        MultiSpec('text', TimeStampSpec('stamp'), sep=u','),
    ]

    def __bytes__(self):
        return text_type(self).encode('utf-8')

    def __str__(self):
        return u','.join([stamp.text for stamp in self.text])

    def _pprint(self):
        return u" / ".join([stamp.text for stamp in self.text])


@swap_to_string
class UrlFrame(Frame):
    """A frame containing a URL string.

    The ID3 specification is silent about IRIs and normalized URL
    forms. Mutagen assumes all URLs in files are encoded as Latin 1,
    but string conversion of this frame returns a UTF-8 representation
    for compatibility with other string conversions.

    The only sane way to handle URLs in MP3s is to restrict them to
    ASCII.
    """

    _framespec = [Latin1TextSpec('url')]

    def __bytes__(self):
        return self.url.encode('utf-8')

    def __str__(self):
        return self.url

    def __eq__(self, other):
        return self.url == other

    __hash__ = Frame.__hash__

    def _pprint(self):
        return self.url


class UrlFrameU(UrlFrame):

    @property
    def HashKey(self):
        return '%s:%s' % (self.FrameID, self.url)


class TALB(TextFrame):
    "Album"


class TBPM(NumericTextFrame):
    "Beats per minute"


class TCOM(TextFrame):
    "Composer"


class TCON(TextFrame):
    """Content type (Genre)

    ID3 has several ways genres can be represented; for convenience,
    use the 'genres' property rather than the 'text' attribute.
    """

    from mutagen._constants import GENRES
    GENRES = GENRES

    def __get_genres(self):
        genres = []
        import re
        genre_re = re.compile(r"((?:\((?P<id>[0-9]+|RX|CR)\))*)(?P<str>.+)?")
        for value in self.text:
            # 255 possible entries in id3v1
            if value.isdigit() and int(value) < 256:
                try:
                    genres.append(self.GENRES[int(value)])
                except IndexError:
                    genres.append(u"Unknown")
            elif value == "CR":
                genres.append(u"Cover")
            elif value == "RX":
                genres.append(u"Remix")
            elif value:
                newgenres = []
                genreid, dummy, genrename = genre_re.match(value).groups()

                if genreid:
                    for gid in genreid[1:-1].split(")("):
                        if gid.isdigit() and int(gid) < len(self.GENRES):
                            gid = text_type(self.GENRES[int(gid)])
                            newgenres.append(gid)
                        elif gid == "CR":
                            newgenres.append(u"Cover")
                        elif gid == "RX":
                            newgenres.append(u"Remix")
                        else:
                            newgenres.append(u"Unknown")

                if genrename:
                    # "Unescaping" the first parenthesis
                    if genrename.startswith("(("):
                        genrename = genrename[1:]
                    if genrename not in newgenres:
                        newgenres.append(genrename)

                genres.extend(newgenres)

        return genres

    def __set_genres(self, genres):
        if isinstance(genres, string_types):
            genres = [genres]
        self.text = [self.__decode(g) for g in genres]

    def __decode(self, value):
        if isinstance(value, bytes):
            enc = EncodedTextSpec._encodings[self.encoding][0]
            return value.decode(enc)
        else:
            return value

    genres = property(__get_genres, __set_genres, None,
                      "A list of genres parsed from the raw text data.")

    def _pprint(self):
        return " / ".join(self.genres)


class TCOP(TextFrame):
    "Copyright (c)"


class TCMP(NumericTextFrame):
    "iTunes Compilation Flag"


class TDAT(TextFrame):
    "Date of recording (DDMM)"


class TDEN(TimeStampTextFrame):
    "Encoding Time"


class TDES(TextFrame):
    "iTunes Podcast Description"


class TDOR(TimeStampTextFrame):
    "Original Release Time"


class TDLY(NumericTextFrame):
    "Audio Delay (ms)"


class TDRC(TimeStampTextFrame):
    "Recording Time"


class TDRL(TimeStampTextFrame):
    "Release Time"


class TDTG(TimeStampTextFrame):
    "Tagging Time"


class TENC(TextFrame):
    "Encoder"


class TEXT(TextFrame):
    "Lyricist"


class TFLT(TextFrame):
    "File type"


class TGID(TextFrame):
    "iTunes Podcast Identifier"


class TIME(TextFrame):
    "Time of recording (HHMM)"


class TIT1(TextFrame):
    "Content group description"


class TIT2(TextFrame):
    "Title"


class TIT3(TextFrame):
    "Subtitle/Description refinement"


class TKEY(TextFrame):
    "Starting Key"


class TLAN(TextFrame):
    "Audio Languages"


class TLEN(NumericTextFrame):
    "Audio Length (ms)"


class TMED(TextFrame):
    "Source Media Type"


class TMOO(TextFrame):
    "Mood"


class TOAL(TextFrame):
    "Original Album"


class TOFN(TextFrame):
    "Original Filename"


class TOLY(TextFrame):
    "Original Lyricist"


class TOPE(TextFrame):
    "Original Artist/Performer"


class TORY(NumericTextFrame):
    "Original Release Year"


class TOWN(TextFrame):
    "Owner/Licensee"


class TPE1(TextFrame):
    "Lead Artist/Performer/Soloist/Group"


class TPE2(TextFrame):
    "Band/Orchestra/Accompaniment"


class TPE3(TextFrame):
    "Conductor"


class TPE4(TextFrame):
    "Interpreter/Remixer/Modifier"


class TPOS(NumericPartTextFrame):
    "Part of set"


class TPRO(TextFrame):
    "Produced (P)"


class TPUB(TextFrame):
    "Publisher"


class TRCK(NumericPartTextFrame):
    "Track Number"


class TRDA(TextFrame):
    "Recording Dates"


class TRSN(TextFrame):
    "Internet Radio Station Name"


class TRSO(TextFrame):
    "Internet Radio Station Owner"


class TSIZ(NumericTextFrame):
    "Size of audio data (bytes)"


class TSO2(TextFrame):
    "iTunes Album Artist Sort"


class TSOA(TextFrame):
    "Album Sort Order key"


class TSOC(TextFrame):
    "iTunes Composer Sort"


class TSOP(TextFrame):
    "Perfomer Sort Order key"


class TSOT(TextFrame):
    "Title Sort Order key"


class TSRC(TextFrame):
    "International Standard Recording Code (ISRC)"


class TSSE(TextFrame):
    "Encoder settings"


class TSST(TextFrame):
    "Set Subtitle"


class TYER(NumericTextFrame):
    "Year of recording"


class TXXX(TextFrame):
    """User-defined text data.

    TXXX frames have a 'desc' attribute which is set to any Unicode
    value (though the encoding of the text and the description must be
    the same). Many taggers use this frame to store freeform keys.
    """

    _framespec = [
        EncodingSpec('encoding'),
        EncodedTextSpec('desc'),
        MultiSpec('text', EncodedTextSpec('text'), sep=u'\u0000'),
    ]

    @property
    def HashKey(self):
        return '%s:%s' % (self.FrameID, self.desc)

    def _pprint(self):
        return "%s=%s" % (self.desc, " / ".join(self.text))


class WCOM(UrlFrameU):
    "Commercial Information"


class WCOP(UrlFrame):
    "Copyright Information"


class WFED(UrlFrame):
    "iTunes Podcast Feed"


class WOAF(UrlFrame):
    "Official File Information"


class WOAR(UrlFrameU):
    "Official Artist/Performer Information"


class WOAS(UrlFrame):
    "Official Source Information"


class WORS(UrlFrame):
    "Official Internet Radio Information"


class WPAY(UrlFrame):
    "Payment Information"


class WPUB(UrlFrame):
    "Official Publisher Information"


class WXXX(UrlFrame):
    """User-defined URL data.

    Like TXXX, this has a freeform description associated with it.
    """

    _framespec = [
        EncodingSpec('encoding'),
        EncodedTextSpec('desc'),
        Latin1TextSpec('url'),
    ]

    @property
    def HashKey(self):
        return '%s:%s' % (self.FrameID, self.desc)


class PairedTextFrame(Frame):
    """Paired text strings.

    Some ID3 frames pair text strings, to associate names with a more
    specific involvement in the song. The 'people' attribute of these
    frames contains a list of pairs::

        [['trumpet', 'Miles Davis'], ['bass', 'Paul Chambers']]

    Like text frames, these frames also have an encoding attribute.
    """

    _framespec = [
        EncodingSpec('encoding'),
        MultiSpec('people',
                  EncodedTextSpec('involvement'),
                  EncodedTextSpec('person'))
    ]

    def __eq__(self, other):
        return self.people == other

    __hash__ = Frame.__hash__


class TIPL(PairedTextFrame):
    "Involved People List"


class TMCL(PairedTextFrame):
    "Musicians Credits List"


class IPLS(TIPL):
    "Involved People List"


class BinaryFrame(Frame):
    """Binary data

    The 'data' attribute contains the raw byte string.
    """

    _framespec = [BinaryDataSpec('data')]

    def __eq__(self, other):
        return self.data == other

    __hash__ = Frame.__hash__


class MCDI(BinaryFrame):
    "Binary dump of CD's TOC"


class ETCO(Frame):
    """Event timing codes."""

    _framespec = [
        ByteSpec("format"),
        KeyEventSpec("events"),
    ]

    def __eq__(self, other):
        return self.events == other

    __hash__ = Frame.__hash__


class MLLT(Frame):
    """MPEG location lookup table.

    This frame's attributes may be changed in the future based on
    feedback from real-world use.
    """

    _framespec = [
        SizedIntegerSpec('frames', 2),
        SizedIntegerSpec('bytes', 3),
        SizedIntegerSpec('milliseconds', 3),
        ByteSpec('bits_for_bytes'),
        ByteSpec('bits_for_milliseconds'),
        BinaryDataSpec('data'),
    ]

    def __eq__(self, other):
        return self.data == other

    __hash__ = Frame.__hash__


class SYTC(Frame):
    """Synchronised tempo codes.

    This frame's attributes may be changed in the future based on
    feedback from real-world use.
    """

    _framespec = [
        ByteSpec("format"),
        BinaryDataSpec("data"),
    ]

    def __eq__(self, other):
        return self.data == other

    __hash__ = Frame.__hash__


@swap_to_string
class USLT(Frame):
    """Unsynchronised lyrics/text transcription.

    Lyrics have a three letter ISO language code ('lang'), a
    description ('desc'), and a block of plain text ('text').
    """

    _framespec = [
        EncodingSpec('encoding'),
        StringSpec('lang', 3),
        EncodedTextSpec('desc'),
        EncodedTextSpec('text'),
    ]

    @property
    def HashKey(self):
        return '%s:%s:%s' % (self.FrameID, self.desc, self.lang)

    def __bytes__(self):
        return self.text.encode('utf-8')

    def __str__(self):
        return self.text

    def __eq__(self, other):
        return self.text == other

    __hash__ = Frame.__hash__


@swap_to_string
class SYLT(Frame):
    """Synchronised lyrics/text."""

    _framespec = [
        EncodingSpec('encoding'),
        StringSpec('lang', 3),
        ByteSpec('format'),
        ByteSpec('type'),
        EncodedTextSpec('desc'),
        SynchronizedTextSpec('text'),
    ]

    @property
    def HashKey(self):
        return '%s:%s:%s' % (self.FrameID, self.desc, self.lang)

    def __eq__(self, other):
        return str(self) == other

    __hash__ = Frame.__hash__

    def __str__(self):
        return u"".join(text for (text, time) in self.text)

    def __bytes__(self):
        return text_type(self).encode("utf-8")


class COMM(TextFrame):
    """User comment.

    User comment frames have a descrption, like TXXX, and also a three
    letter ISO language code in the 'lang' attribute.
    """

    _framespec = [
        EncodingSpec('encoding'),
        StringSpec('lang', 3),
        EncodedTextSpec('desc'),
        MultiSpec('text', EncodedTextSpec('text'), sep=u'\u0000'),
    ]

    @property
    def HashKey(self):
        return '%s:%s:%s' % (self.FrameID, self.desc, self.lang)

    def _pprint(self):
        return "%s=%s=%s" % (self.desc, self.lang, " / ".join(self.text))


class RVA2(Frame):
    """Relative volume adjustment (2).

    This frame is used to implemented volume scaling, and in
    particular, normalization using ReplayGain.

    Attributes:

    * desc -- description or context of this adjustment
    * channel -- audio channel to adjust (master is 1)
    * gain -- a + or - dB gain relative to some reference level
    * peak -- peak of the audio as a floating point number, [0, 1]

    When storing ReplayGain tags, use descriptions of 'album' and
    'track' on channel 1.
    """

    _framespec = [
        Latin1TextSpec('desc'),
        ChannelSpec('channel'),
        VolumeAdjustmentSpec('gain'),
        VolumePeakSpec('peak'),
    ]

    _channels = ["Other", "Master volume", "Front right", "Front left",
                 "Back right", "Back left", "Front centre", "Back centre",
                 "Subwoofer"]

    @property
    def HashKey(self):
        return '%s:%s' % (self.FrameID, self.desc)

    def __eq__(self, other):
        try:
            return ((str(self) == other) or
                    (self.desc == other.desc and
                     self.channel == other.channel and
                     self.gain == other.gain and
                     self.peak == other.peak))
        except AttributeError:
            return False

    __hash__ = Frame.__hash__

    def __str__(self):
        return "%s: %+0.4f dB/%0.4f" % (
            self._channels[self.channel], self.gain, self.peak)


class EQU2(Frame):
    """Equalisation (2).

    Attributes:
    method -- interpolation method (0 = band, 1 = linear)
    desc -- identifying description
    adjustments -- list of (frequency, vol_adjustment) pairs
    """

    _framespec = [
        ByteSpec("method"),
        Latin1TextSpec("desc"),
        VolumeAdjustmentsSpec("adjustments"),
    ]

    def __eq__(self, other):
        return self.adjustments == other

    __hash__ = Frame.__hash__

    @property
    def HashKey(self):
        return '%s:%s' % (self.FrameID, self.desc)


# class RVAD: unsupported
# class EQUA: unsupported


class RVRB(Frame):
    """Reverb."""

    _framespec = [
        SizedIntegerSpec('left', 2),
        SizedIntegerSpec('right', 2),
        ByteSpec('bounce_left'),
        ByteSpec('bounce_right'),
        ByteSpec('feedback_ltl'),
        ByteSpec('feedback_ltr'),
        ByteSpec('feedback_rtr'),
        ByteSpec('feedback_rtl'),
        ByteSpec('premix_ltr'),
        ByteSpec('premix_rtl'),
    ]

    def __eq__(self, other):
        return (self.left, self.right) == other

    __hash__ = Frame.__hash__


class APIC(Frame):
    """Attached (or linked) Picture.

    Attributes:

    * encoding -- text encoding for the description
    * mime -- a MIME type (e.g. image/jpeg) or '-->' if the data is a URI
    * type -- the source of the image (3 is the album front cover)
    * desc -- a text description of the image
    * data -- raw image data, as a byte string

    Mutagen will automatically compress large images when saving tags.
    """

    _framespec = [
        EncodingSpec('encoding'),
        Latin1TextSpec('mime'),
        PictureTypeSpec('type'),
        EncodedTextSpec('desc'),
        BinaryDataSpec('data'),
    ]

    def __eq__(self, other):
        return self.data == other

    __hash__ = Frame.__hash__

    @property
    def HashKey(self):
        return '%s:%s' % (self.FrameID, self.desc)

    def _validate_from_22(self, other, checker):
        if checker.name == "mime":
            self.mime = other.mime.decode("ascii", "ignore")
        else:
            super(APIC, self)._validate_from_22(other, checker)

    def _pprint(self):
        type_desc = text_type(self.type)
        if hasattr(self.type, "_pprint"):
            type_desc = self.type._pprint()

        return "%s, %s (%s, %d bytes)" % (
            type_desc, self.desc, self.mime, len(self.data))


class PCNT(Frame):
    """Play counter.

    The 'count' attribute contains the (recorded) number of times this
    file has been played.

    This frame is basically obsoleted by POPM.
    """

    _framespec = [IntegerSpec('count')]

    def __eq__(self, other):
        return self.count == other

    __hash__ = Frame.__hash__

    def __pos__(self):
        return self.count

    def _pprint(self):
        return text_type(self.count)


class POPM(FrameOpt):
    """Popularimeter.

    This frame keys a rating (out of 255) and a play count to an email
    address.

    Attributes:

    * email -- email this POPM frame is for
    * rating -- rating from 0 to 255
    * count -- number of times the files has been played (optional)
    """

    _framespec = [
        Latin1TextSpec('email'),
        ByteSpec('rating'),
    ]

    _optionalspec = [IntegerSpec('count')]

    @property
    def HashKey(self):
        return '%s:%s' % (self.FrameID, self.email)

    def __eq__(self, other):
        return self.rating == other

    __hash__ = FrameOpt.__hash__

    def __pos__(self):
        return self.rating

    def _pprint(self):
        return "%s=%r %r/255" % (
            self.email, getattr(self, 'count', None), self.rating)


class GEOB(Frame):
    """General Encapsulated Object.

    A blob of binary data, that is not a picture (those go in APIC).

    Attributes:

    * encoding -- encoding of the description
    * mime -- MIME type of the data or '-->' if the data is a URI
    * filename -- suggested filename if extracted
    * desc -- text description of the data
    * data -- raw data, as a byte string
    """

    _framespec = [
        EncodingSpec('encoding'),
        Latin1TextSpec('mime'),
        EncodedTextSpec('filename'),
        EncodedTextSpec('desc'),
        BinaryDataSpec('data'),
    ]

    @property
    def HashKey(self):
        return '%s:%s' % (self.FrameID, self.desc)

    def __eq__(self, other):
        return self.data == other

    __hash__ = Frame.__hash__


class RBUF(FrameOpt):
    """Recommended buffer size.

    Attributes:

    * size -- recommended buffer size in bytes
    * info -- if ID3 tags may be elsewhere in the file (optional)
    * offset -- the location of the next ID3 tag, if any

    Mutagen will not find the next tag itself.
    """

    _framespec = [SizedIntegerSpec('size', 3)]

    _optionalspec = [
        ByteSpec('info'),
        SizedIntegerSpec('offset', 4),
    ]

    def __eq__(self, other):
        return self.size == other

    __hash__ = FrameOpt.__hash__

    def __pos__(self):
        return self.size


@swap_to_string
class AENC(FrameOpt):
    """Audio encryption.

    Attributes:

    * owner -- key identifying this encryption type
    * preview_start -- unencrypted data block offset
    * preview_length -- number of unencrypted blocks
    * data -- data required for decryption (optional)

    Mutagen cannot decrypt files.
    """

    _framespec = [
        Latin1TextSpec('owner'),
        SizedIntegerSpec('preview_start', 2),
        SizedIntegerSpec('preview_length', 2),
    ]

    _optionalspec = [BinaryDataSpec('data')]

    @property
    def HashKey(self):
        return '%s:%s' % (self.FrameID, self.owner)

    def __bytes__(self):
        return self.owner.encode('utf-8')

    def __str__(self):
        return self.owner

    def __eq__(self, other):
        return self.owner == other

    __hash__ = FrameOpt.__hash__


class LINK(FrameOpt):
    """Linked information.

    Attributes:

    * frameid -- the ID of the linked frame
    * url -- the location of the linked frame
    * data -- further ID information for the frame
    """

    _framespec = [
        StringSpec('frameid', 4),
        Latin1TextSpec('url'),
    ]

    _optionalspec = [BinaryDataSpec('data')]

    @property
    def HashKey(self):
        try:
            return "%s:%s:%s:%s" % (
                self.FrameID, self.frameid, self.url, _bytes2key(self.data))
        except AttributeError:
            return "%s:%s:%s" % (self.FrameID, self.frameid, self.url)

    def __eq__(self, other):
        try:
            return (self.frameid, self.url, self.data) == other
        except AttributeError:
            return (self.frameid, self.url) == other

    __hash__ = FrameOpt.__hash__


class POSS(Frame):
    """Position synchronisation frame

    Attribute:

    * format -- format of the position attribute (frames or milliseconds)
    * position -- current position of the file
    """

    _framespec = [
        ByteSpec('format'),
        IntegerSpec('position'),
    ]

    def __pos__(self):
        return self.position

    def __eq__(self, other):
        return self.position == other

    __hash__ = Frame.__hash__


class UFID(Frame):
    """Unique file identifier.

    Attributes:

    * owner -- format/type of identifier
    * data -- identifier
    """

    _framespec = [
        Latin1TextSpec('owner'),
        BinaryDataSpec('data'),
    ]

    @property
    def HashKey(self):
        return '%s:%s' % (self.FrameID, self.owner)

    def __eq__(s, o):
        if isinstance(o, UFI):
            return s.owner == o.owner and s.data == o.data
        else:
            return s.data == o

    __hash__ = Frame.__hash__

    def _pprint(self):
        return "%s=%r" % (self.owner, self.data)


@swap_to_string
class USER(Frame):
    """Terms of use.

    Attributes:

    * encoding -- text encoding
    * lang -- ISO three letter language code
    * text -- licensing terms for the audio
    """

    _framespec = [
        EncodingSpec('encoding'),
        StringSpec('lang', 3),
        EncodedTextSpec('text'),
    ]

    @property
    def HashKey(self):
        return '%s:%s' % (self.FrameID, self.lang)

    def __bytes__(self):
        return self.text.encode('utf-8')

    def __str__(self):
        return self.text

    def __eq__(self, other):
        return self.text == other

    __hash__ = Frame.__hash__

    def _pprint(self):
        return "%r=%s" % (self.lang, self.text)


@swap_to_string
class OWNE(Frame):
    """Ownership frame."""

    _framespec = [
        EncodingSpec('encoding'),
        Latin1TextSpec('price'),
        StringSpec('date', 8),
        EncodedTextSpec('seller'),
    ]

    def __bytes__(self):
        return self.seller.encode('utf-8')

    def __str__(self):
        return self.seller

    def __eq__(self, other):
        return self.seller == other

    __hash__ = Frame.__hash__


class COMR(FrameOpt):
    """Commercial frame."""

    _framespec = [
        EncodingSpec('encoding'),
        Latin1TextSpec('price'),
        StringSpec('valid_until', 8),
        Latin1TextSpec('contact'),
        ByteSpec('format'),
        EncodedTextSpec('seller'),
        EncodedTextSpec('desc'),
    ]

    _optionalspec = [
        Latin1TextSpec('mime'),
        BinaryDataSpec('logo'),
    ]

    @property
    def HashKey(self):
        return '%s:%s' % (self.FrameID, _bytes2key(self._writeData()))

    def __eq__(self, other):
        return self._writeData() == other._writeData()

    __hash__ = FrameOpt.__hash__


@swap_to_string
class ENCR(Frame):
    """Encryption method registration.

    The standard does not allow multiple ENCR frames with the same owner
    or the same method. Mutagen only verifies that the owner is unique.
    """

    _framespec = [
        Latin1TextSpec('owner'),
        ByteSpec('method'),
        BinaryDataSpec('data'),
    ]

    @property
    def HashKey(self):
        return "%s:%s" % (self.FrameID, self.owner)

    def __bytes__(self):
        return self.data

    def __eq__(self, other):
        return self.data == other

    __hash__ = Frame.__hash__


@swap_to_string
class GRID(FrameOpt):
    """Group identification registration."""

    _framespec = [
        Latin1TextSpec('owner'),
        ByteSpec('group'),
    ]

    _optionalspec = [BinaryDataSpec('data')]

    @property
    def HashKey(self):
        return '%s:%s' % (self.FrameID, self.group)

    def __pos__(self):
        return self.group

    def __bytes__(self):
        return self.owner.encode('utf-8')

    def __str__(self):
        return self.owner

    def __eq__(self, other):
        return self.owner == other or self.group == other

    __hash__ = FrameOpt.__hash__


@swap_to_string
class PRIV(Frame):
    """Private frame."""

    _framespec = [
        Latin1TextSpec('owner'),
        BinaryDataSpec('data'),
    ]

    @property
    def HashKey(self):
        return '%s:%s:%s' % (
            self.FrameID, self.owner, _bytes2key(self.data))

    def __bytes__(self):
        return self.data

    def __eq__(self, other):
        return self.data == other

    def _pprint(self):
        return "%s=%r" % (self.owner, self.data)

    __hash__ = Frame.__hash__


@swap_to_string
class SIGN(Frame):
    """Signature frame."""

    _framespec = [
        ByteSpec('group'),
        BinaryDataSpec('sig'),
    ]

    @property
    def HashKey(self):
        return '%s:%s:%s' % (self.FrameID, self.group, _bytes2key(self.sig))

    def __bytes__(self):
        return self.sig

    def __eq__(self, other):
        return self.sig == other

    __hash__ = Frame.__hash__


class SEEK(Frame):
    """Seek frame.

    Mutagen does not find tags at seek offsets.
    """

    _framespec = [IntegerSpec('offset')]

    def __pos__(self):
        return self.offset

    def __eq__(self, other):
        return self.offset == other

    __hash__ = Frame.__hash__


class ASPI(Frame):
    """Audio seek point index.

    Attributes: S, L, N, b, and Fi. For the meaning of these, see
    the ID3v2.4 specification. Fi is a list of integers.
    """
    _framespec = [
        SizedIntegerSpec("S", 4),
        SizedIntegerSpec("L", 4),
        SizedIntegerSpec("N", 2),
        ByteSpec("b"),
        ASPIIndexSpec("Fi"),
    ]

    def __eq__(self, other):
        return self.Fi == other

    __hash__ = Frame.__hash__


# ID3v2.2 frames
class UFI(UFID):
    "Unique File Identifier"


class TT1(TIT1):
    "Content group description"


class TT2(TIT2):
    "Title"


class TT3(TIT3):
    "Subtitle/Description refinement"


class TP1(TPE1):
    "Lead Artist/Performer/Soloist/Group"


class TP2(TPE2):
    "Band/Orchestra/Accompaniment"


class TP3(TPE3):
    "Conductor"


class TP4(TPE4):
    "Interpreter/Remixer/Modifier"


class TCM(TCOM):
    "Composer"


class TXT(TEXT):
    "Lyricist"


class TLA(TLAN):
    "Audio Language(s)"


class TCO(TCON):
    "Content Type (Genre)"


class TAL(TALB):
    "Album"


class TPA(TPOS):
    "Part of set"


class TRK(TRCK):
    "Track Number"


class TRC(TSRC):
    "International Standard Recording Code (ISRC)"


class TYE(TYER):
    "Year of recording"


class TDA(TDAT):
    "Date of recording (DDMM)"


class TIM(TIME):
    "Time of recording (HHMM)"


class TRD(TRDA):
    "Recording Dates"


class TMT(TMED):
    "Source Media Type"


class TFT(TFLT):
    "File Type"


class TBP(TBPM):
    "Beats per minute"


class TCP(TCMP):
    "iTunes Compilation Flag"


class TCR(TCOP):
    "Copyright (C)"


class TPB(TPUB):
    "Publisher"


class TEN(TENC):
    "Encoder"


class TSS(TSSE):
    "Encoder settings"


class TOF(TOFN):
    "Original Filename"


class TLE(TLEN):
    "Audio Length (ms)"


class TSI(TSIZ):
    "Audio Data size (bytes)"


class TDY(TDLY):
    "Audio Delay (ms)"


class TKE(TKEY):
    "Starting Key"


class TOT(TOAL):
    "Original Album"


class TOA(TOPE):
    "Original Artist/Perfomer"


class TOL(TOLY):
    "Original Lyricist"


class TOR(TORY):
    "Original Release Year"


class TXX(TXXX):
    "User-defined Text"


class WAF(WOAF):
    "Official File Information"


class WAR(WOAR):
    "Official Artist/Performer Information"


class WAS(WOAS):
    "Official Source Information"


class WCM(WCOM):
    "Commercial Information"


class WCP(WCOP):
    "Copyright Information"


class WPB(WPUB):
    "Official Publisher Information"


class WXX(WXXX):
    "User-defined URL"


class IPL(IPLS):
    "Involved people list"


class MCI(MCDI):
    "Binary dump of CD's TOC"


class ETC(ETCO):
    "Event timing codes"


class MLL(MLLT):
    "MPEG location lookup table"


class STC(SYTC):
    "Synced tempo codes"


class ULT(USLT):
    "Unsychronised lyrics/text transcription"


class SLT(SYLT):
    "Synchronised lyrics/text"


class COM(COMM):
    "Comment"


# class RVA(RVAD)
# class EQU(EQUA)


class REV(RVRB):
    "Reverb"


class PIC(APIC):
    """Attached Picture.

    The 'mime' attribute of an ID3v2.2 attached picture must be either
    'PNG' or 'JPG'.
    """

    _framespec = [
        EncodingSpec('encoding'),
        StringSpec('mime', 3),
        PictureTypeSpec('type'),
        EncodedTextSpec('desc'),
        BinaryDataSpec('data')
    ]

    def _to_other(self, other):
        if not isinstance(other, APIC):
            raise TypeError

        other.encoding = self.encoding
        other.mime = self.mime
        other.type = self.type
        other.desc = self.desc
        other.data = self.data


class GEO(GEOB):
    "General Encapsulated Object"


class CNT(PCNT):
    "Play counter"


class POP(POPM):
    "Popularimeter"


class BUF(RBUF):
    "Recommended buffer size"


class CRM(Frame):
    """Encrypted meta frame"""
    _framespec = [Latin1TextSpec('owner'), Latin1TextSpec('desc'),
                  BinaryDataSpec('data')]

    def __eq__(self, other):
        return self.data == other
    __hash__ = Frame.__hash__


class CRA(AENC):
    "Audio encryption"


class LNK(LINK):
    """Linked information"""

    _framespec = [
        StringSpec('frameid', 3),
        Latin1TextSpec('url')
    ]

    _optionalspec = [BinaryDataSpec('data')]

    def _to_other(self, other):
        if not isinstance(other, LINK):
            raise TypeError

        if isinstance(other, LNK):
            other.frameid = self.frameid
        else:
            try:
                other.frameid = Frames_2_2[self.frameid].__bases__[0].__name__
            except KeyError:
                other.frameid = self.frameid.ljust(4)
        other.url = self.url
        if hasattr(self, "data"):
            other.data = self.data


Frames = {}
"""All supported ID3v2.3/4 frames, keyed by frame name."""


Frames_2_2 = {}
"""All supported ID3v2.2 frames, keyed by frame name."""


k, v = None, None
for k, v in iteritems(globals()):
    if isinstance(v, type) and issubclass(v, Frame):
        v.__module__ = "mutagen.id3"

        if len(k) == 3:
            Frames_2_2[k] = v
        elif len(k) == 4:
            Frames[k] = v

try:
    del k
    del v
except NameError:
    pass
