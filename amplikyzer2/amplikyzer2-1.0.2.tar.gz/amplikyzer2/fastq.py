"""
fastq module for amplikyzer2
Provides class FASTQFile which is a FASTQ reader for DNA sequences.
Quality scores are currently assumed to be in Sanger / Illumina 1.8+ format.
"""

import gzip


class FormatError(Exception):
    pass


def _make_translations(invalid_value):
    """Return byte translation tables to be used for base and quality parsing."""
    from .alphabets import GENOMIC
    valid_bases = GENOMIC.encode("ascii").upper()
    valid_quals = range(0, 41)
    qual_offset = 33

    bytes_ = bytes(range(256))

    trans_bases = [invalid_value] * len(bytes_)
    for uppercase, lowercase in zip(valid_bases.upper(), valid_bases.lower()):
        trans_bases[uppercase] = uppercase
        trans_bases[lowercase] = uppercase
    trans_quals = [invalid_value] * len(bytes_)
    for qual in valid_quals:
        trans_quals[qual + qual_offset] = qual

    trans_bases = bytes.maketrans(bytes_, bytes(trans_bases))
    trans_quals = bytes.maketrans(bytes_, bytes(trans_quals))
    return trans_bases, trans_quals


class Read:
    """DNA Read from FASTQ file.
    Attributes:
     `index`: `int`, index of read in FASTQ file
     `name`:  `str`, read identifier
     `seq`:   `str`, dna base sequence
     `qual`:  `tuple` of `int`, base quality values (-10log10-representation)
    """

    _INVALID_VALUE = 255
    """Indicator for erroneous base or quality values."""

    (_TRANS_BASES, _TRANS_QUALS) = _make_translations(_INVALID_VALUE)
    """Translation tables for base and quality parsing."""

    def __init__(self, index, name, seq, qual):
        """
        `index`: `int`, index of read in FASTQ file
        `name`:  `bytes`, ASCII-encoded name of the read
        `seq:`   `bytearray`, ASCII-encoded base sequence
        `qual`:  `bytearray`, ASCII-encoded Phred quality scores
        """
        self.index = index
        self.name = name.decode("ascii")
        self.bases = seq.translate(Read._TRANS_BASES)
        self.qual = qual.translate(Read._TRANS_QUALS)
        if Read._INVALID_VALUE in self.bases:
            i = self.bases.index(Read._INVALID_VALUE)
            c = seq[i]
            c = chr(c) if 32 <= c <= 127 else '\\x{:02X}'.format(c)
            raise FormatError("Invalid sequence character '{}' at position {}.".format(c, i))
        if Read._INVALID_VALUE in self.qual:
            i = self.qual.index(Read._INVALID_VALUE)
            c = qual[i]
            c = chr(c) if 32 <= c <= 127 else '\\x{:02X}'.format(c)
            raise FormatError("Invalid quality value '{}' at position {}.".format(c, i))
        self.bases = self.bases.decode("ascii")
        self.qual = tuple(self.qual)


class FASTQFile:
    """FASTQ reader for (IUPAC) DNA sequences with Illumina 1.8+ quality scores."""

    def __init__(self, filename):
        self.filename = filename

    def reads(self):
        """Yield instances of class `Read` for each read in the input file."""
        filename = self.filename
        open_ = gzip.open if filename.endswith(".gz") else open
        with open_(filename, mode="rb") as file:
            # NOTE: in binary mode readline does not recognize single '\r's as
            #       line separators. Does any sane being still use single '\r's?
            lines = (line.rstrip(b"\r\n") for line in file)
            for index, identifier_line in enumerate(lines):
                try:
                    (name, seq, qual) = self._get_read(identifier_line, lines)
                    yield Read(index, name, seq, qual)
                except FormatError as e:
                    msg = "FASTQ: {}. At read {} in file {}.".format(e, index, filename)
                    raise FormatError(msg) from e

    def _get_read(self, identifier_line, lines):
        if not identifier_line.startswith(b"@"):
            raise FormatError("Indentifier line not starting with '@'.")
        name = identifier_line[1:]
        seq = bytearray()
        for line in lines:
            if line.startswith(b"+"):
                break
            seq.extend(line)
        else:
            raise FormatError("EOF while reading sequence.")
        repeated_name = line[1:]
        if repeated_name and repeated_name != name:
            raise FormatError("Sequence identifier mismatch at '+' line.")
        qual = bytearray()
        for line in lines:
            qual.extend(line)
            if len(qual) == len(seq):
                break
            elif len(qual) > len(seq):
                raise FormatError("Number of quality values exceeded sequence length.")
        else:
            raise FormatError("EOF while reading quality values.")
        return (name, seq, qual)
