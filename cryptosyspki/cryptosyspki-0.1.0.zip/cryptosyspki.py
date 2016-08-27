#! python2

"""A Python interface to CryptoSys PKI <http://www.cryptosys.net/pki/>."""

# cryptosyspki.py

# ************************** LICENSE *****************************************
# Copyright (C) 2016 David Ireland, DI Management Services Pty Limited.
# <www.di-mgt.com.au> <www.cryptosys.net>
# This code is provided 'as-is' without any express or implied warranty.
# Free license is hereby granted to use this code as part of an application
# provided this license notice is left intact. You are *not* licensed to
# share any of this code in any form of mass distribution, including, but not
# limited to, reposting on other web sites or in any source code repository.
# ****************************************************************************

from ctypes import windll, create_string_buffer, c_char_p, c_void_p, c_int

__version__ = "0.1.1"
# Added sphinx-compatible comments to public constants [2016-08-19]

# OUR EXPORTED CLASSES
__all__ = (
    'PKIError',
    'Asn1', 'Cipher', 'Cms', 'Cnv', 'Ecc', 'Gen', 'Hash', 'Hmac', 'Ocsp',
    'Pbe', 'Pem', 'Pfx', 'Pwd', 'Rng', 'Rsa', 'Sig', 'Smime', 'Wipe', 'X509'
)

# Our global DLL object for CryptoSys PKI
_dipki = windll.diCrPKI

# Global constants
_INTMAX = 2147483647
_INTMIN = -2147483648


def _isanint(v):
    try: v = int(v)
    except: pass
    return isinstance(v, int)


class PKIError(Exception):
    """Raised when a call to a core PKI library function returns an error, or some obviously wrong parameter is detected."""

    def __init__(self, value):
        """."""
        self.value = value

    def __str__(self):
        """Behave differently if value is an integer or not."""
        if (_isanint(self.value)):
            n = int(self.value)
            s1 = "ERROR CODE %d: %s" % (n, Gen.error_lookup(n))
        else:
            s1 = "ERROR: %s" % (self.value)
        se = Gen.last_error()
        return "%s%s" % (s1, ": " + se if se else "")
        return s1


class Asn1:
    """Utilities to analyze ASN.1 files."""

    class Opts():
        """Bitwise flags for text_dump()."""
        NOCOMMENTS = 0x100000  #: Hide the comments
        ADDLEVELS  = 0x800000  #: Show level numbers

    @staticmethod
    def type(asn1file):
        """Describe the type of ASN.1 data."""
        nc = _dipki.ASN1_Type(None, 0, asn1file, 0)
        if (nc < 0): raise PKIError(-nc)
        if (nc == 0): return ""
        buf = create_string_buffer(nc + 1)
        nc = _dipki.ASN1_Type(buf, nc, asn1file, 0)
        return str(buf.value)

    @staticmethod
    def text_dump(outputfile, asn1file, opts=0):
        """Dump details of an ASN.1 formatted data file to a text file."""
        n = _dipki.ASN1_TextDump(outputfile, asn1file, opts)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n


class Cipher:
    """Generic block cipher functions."""
    # CONSTANTS
    class Alg:
        """Block cipher algorithms."""
        TDEA   = 0x10  #: Triple DES (3DES, des-ede3)
        AES128 = 0x20  #: AES-128
        AES192 = 0x30  #: AES-192
        AES256 = 0x40  #: AES-256

    class Mode:
        """Block cipher modes."""
        ECB = 0      #: Electronic Code Book mode (default)
        CBC = 0x100  #: Cipher Block Chaining mode
        OFB = 0x200  #: Output Feedback mode 
        CFB = 0x300  #: Cipher Feedback mode
        CTR = 0x400  #: Counter mode

    class Pad:
        """Block cipher padding options."""
        DEFAULT = 0             #: Use default padding
        NOPAD        = 0x10000  #: No padding is added
        PKCS5        = 0x20000  #: Padding scheme in PKCS#5
        ONEANDZEROES = 0x30000  #: Pads with 0x80 followed by as many zero bytes necessary to fill the block
        ANSIX923     = 0x40000  #: Padding scheme in ANSI X9.23
        W3C          = 0x50000  #: Padding scheme in W3C XMLENC

    class Opts:
        DEFAULT = 0  #: Use default options
        PREFIXIV = 0x1000  #: Prepend the IV before the ciphertext in the output file (ignored for ECB mode)

    # Internal lookup
    _blocksize = {Alg.TDEA: 8, Alg.AES128: 16, Alg.AES192: 16, Alg.AES256: 16}
    _keysize = {Alg.TDEA: 24, Alg.AES128: 16, Alg.AES192: 24, Alg.AES256: 32}

    @staticmethod
    def blockbytes(alg):
        """Return block size in bytes."""
        return Cipher._blocksize[alg]

    @staticmethod
    def keybytes(alg):
        """Return key size in bytes."""
        return Cipher._keysize[alg]

    @staticmethod
    def encrypt(data, key, iv=None, algmodepad=None, alg=None, mode=Mode.ECB, pad=Pad.DEFAULT):
        """Encrypt data."""
        if (algmodepad is None or len(algmodepad) == 0):
            if (alg is None): raise PKIError("Cipher algorithm must be specified")
            noptions = int(alg) | int(mode) | int(pad)
        else:
            noptions = 0
        ivlen = 0 if iv is None else len(iv)  # Careful not to call len(None)
        n = _dipki.CIPHER_EncryptBytes2(None, 0, bytes(data), len(data), bytes(key), len(key), bytes(iv), ivlen, algmodepad, noptions)
        if (n < 0): raise PKIError(-n)
        buf = create_string_buffer(n)
        n = _dipki.CIPHER_EncryptBytes2(buf, n, bytes(data), len(data), bytes(key), len(key), bytes(iv), ivlen, algmodepad, noptions)
        return bytearray(buf.raw)

    @staticmethod
    def decrypt(data, key, iv=None, algmodepad=None, alg=None, mode=Mode.ECB, pad=Pad.DEFAULT):
        """Decrypt data."""
        if (algmodepad is None or len(algmodepad) == 0):
            if (alg is None): raise PKIError("Cipher algorithm must be specified")
            noptions = int(alg) + int(mode) + int(pad)
        else:
            noptions = 0
        ivlen = 0 if iv is None else len(iv)  # Careful not to call len(None)
        dlen = len(data)
        buf = create_string_buffer(dlen)
        n = _dipki.CIPHER_DecryptBytes2(buf, dlen, bytes(data), len(data), bytes(key), len(key), bytes(iv), ivlen, algmodepad, noptions)
        if (n < 0): raise PKIError(-n)
        # Shorten output if necessary
        return bytes(buf.raw)[:n]

    @staticmethod
    def encrypt_block(data, key, iv=None, alg=Alg.TDEA, mode=Mode.ECB):
        """Encrypt a block of data. Must be an exact multiple of block length."""
        noptions = int(alg) | int(mode) | int(Cipher.Pad.NOPAD)
        ivlen = 0 if iv is None else len(iv)  # Careful not to call len(None)
        # Output is always the same length as the input
        n = len(data)
        buf = create_string_buffer(n)
        n = _dipki.CIPHER_EncryptBytes2(buf, n, bytes(data), len(data), bytes(key), len(key), bytes(iv), ivlen, None, noptions)
        if (n < 0): raise PKIError(-n)
        return bytearray(buf.raw)

    @staticmethod
    def decrypt_block(data, key, iv=None, alg=Alg.TDEA, mode=Mode.ECB):
        """Decrypt a block of data. Must be an exact multiple of block length."""
        noptions = int(alg) | int(mode) | int(Cipher.Pad.NOPAD)
        ivlen = 0 if iv is None else len(iv)  # Careful not to call len(None)
        # Output is always the same length as the input
        n = len(data)
        buf = create_string_buffer(n)
        n = _dipki.CIPHER_DecryptBytes2(buf, n, bytes(data), len(data), bytes(key), len(key), bytes(iv), ivlen, None, noptions)
        if (n < 0): raise PKIError(-n)
        return bytearray(buf.raw)

    @staticmethod
    def file_encrypt(fileout, filein, key, iv, algmodepad=None, alg=None, mode=Mode.ECB, pad=Pad.DEFAULT, opts=Opts.DEFAULT):
        """Encrypt a file."""
        if (algmodepad is None or len(algmodepad) == 0):
            if (alg is None): raise PKIError("Cipher algorithm must be specified")
            noptions = int(alg) | int(mode) | int(pad)
        else:
            noptions = 0
        if (opts != 0):
            noptions |= int(opts)
        n = _dipki.CIPHER_FileEncrypt(fileout, filein, bytes(key), len(key), bytes(iv), len(iv), algmodepad, noptions)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def file_decrypt(fileout, filein, key, iv, algmodepad=None, alg=None, mode=Mode.ECB, pad=Pad.DEFAULT, opts=Opts.DEFAULT):
        """Decrypt a file."""
        if (algmodepad is None or len(algmodepad) == 0):
            if (alg is None): raise PKIError("Cipher algorithm must be specified")
            noptions = int(alg) | int(mode) | int(pad)
        else:
            noptions = 0
        if (opts != 0):
            noptions |= int(opts)
        n = _dipki.CIPHER_FileDecrypt(fileout, filein, bytes(key), len(key), bytes(iv), len(iv), algmodepad, noptions)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def key_wrap(data, kek, alg):
        """Wrap (encrypt) key material with a key-encryption key."""
        n = _dipki.CIPHER_KeyWrap(None, 0, data, len(data), kek, len(kek), alg)
        if (n < 0): raise PKIError(-n)
        buf = create_string_buffer(n)
        n = _dipki.CIPHER_KeyWrap(buf, n, data, len(data), kek, len(kek), alg)
        return bytes(buf.raw)[:n]

    @staticmethod
    def key_unwrap(data, kek, alg):
        """Unwrap (decrypt) key material with a key-encryption key."""
        n = _dipki.CIPHER_KeyUnwrap(None, 0, data, len(data), kek, len(kek), alg)
        if (n < 0): raise PKIError(-n)
        buf = create_string_buffer(n)
        n = _dipki.CIPHER_KeyUnwrap(buf, n, data, len(data), kek, len(kek), alg)
        return bytes(buf.raw)[:n]

    @staticmethod
    def pad(data, alg, pad=Pad.PKCS5):
        """Pad byte array for block cipher."""
        blklen = Cipher._blocksize[alg]
        n = _dipki.PAD_BytesBlock(None, 0, data, len(data), blklen, pad)
        if (n < 0): raise PKIError(-n)
        buf = create_string_buffer(n)
        n = _dipki.PAD_BytesBlock(buf, n, data, len(data), blklen, pad)
        return bytes(buf.raw)[:n]

    @staticmethod
    def pad_hex(datahex, alg, pad=Pad.PKCS5):
        """Pad hex-encoded string to correct length for ECB and CBC encryption."""
        blklen = Cipher._blocksize[alg]
        n = _dipki.PAD_HexBlock(None, 0, datahex, blklen, pad)
        if (n < 0): raise PKIError(-n)
        buf = create_string_buffer(n)
        n = _dipki.PAD_HexBlock(buf, n, datahex, blklen, pad)
        return bytes(buf.raw)[:n]

    @staticmethod
    def unpad(data, alg, pad=Pad.PKCS5):
        """Remove the padding from an encryption block."""
        blklen = Cipher._blocksize[alg]
        n = len(data)
        buf = create_string_buffer(n)
        n = _dipki.PAD_UnpadBytes(buf, n, data, len(data), blklen, pad)
        return bytes(buf.raw)[:n]

    @staticmethod
    def unpad_hex(datahex, alg, pad=Pad.PKCS5):
        """Remove the padding from a hex-encoded encryption block."""
        blklen = Cipher._blocksize[alg]
        n = len(datahex)
        buf = create_string_buffer(n)
        n = _dipki.PAD_UnpadHex(buf, n, datahex, blklen, pad)
        return bytes(buf.raw)[:n]


class Cms:
    """Create, read and analyze Cryptographic Message Syntax (CMS) objects."""

    class SigDataOpts:
        DEFAULT = 0  #: Use default options
        FORMAT_BASE64     = 0x10000  #: Format output in base64 [default=binary]
        EXCLUDE_CERTS      = 0x0100  #: Exclude X.509 certs from output.
        EXCLUDE_DATA       = 0x0200  #: Exclude data from output.
        CERTS_ONLY         = 0x0400  #: Create a "certs-only" PKCS#7 certficate chain.
        INCLUDE_ATTRS      = 0x0800  #: Include Signed Attributes.
        ADD_SIGNTIME       = 0x1000  #: Add signing time.
        ADD_SMIMECAP       = 0x2000  #: Add S/MIME capabilities.
        NO_OUTER        = 0x2000000  #: Create a "naked" SignedData object with no outerContentInfo as per PKCS#7 v1.6
        ALT_ALGID       = 0x4000000  #: Use alternative (non-standard) signature algorithm identifiers

    class EnvDataOpts:
        DEFAULT = 0  #: Use default options
        FORMAT_BASE64     = 0x10000  #: Format output in base64 [default=binary]
        ALT_ALGID       = 0x4000000  #: Use alternative (non-standard) encryption algorithm identifiers

    class ComprDataOpts:
        DEFAULT = 0
        NO_INFLATE      = 0x1000000  #: Extract the compressed data as is without inflation

    # Local constants
    _BIGFILE = 0x8000000  # Speed up processing of large files (binary-to-binary only)

    @staticmethod
    def make_envdata(outputfile, inputfile, certlist, cipheralg=0, opts=EnvDataOpts.DEFAULT, bigfile=False):
        """Create a CMS enveloped-data object for one or more recipients using their x.509 certificates.
        file --> file
        """
        noptions = opts | cipheralg | (Cms._BIGFILE if bigfile else 0)
        n = _dipki.CMS_MakeEnvData(outputfile, inputfile, certlist, None, 0, noptions)
        # Careful: returns +ve number of recipients or a -ve error code
        if (n < 0): raise PKIError(-n)
        return n    # Number of recipients

    @staticmethod
    def make_envdata_from_string(outputfile, inputdata, certlist, cipheralg=0, opts=EnvDataOpts.DEFAULT):
        """Create a CMS enveloped-data object for one or more recipients using their x.509 certificates.
        string --> file
        """
        noptions = opts | cipheralg
        n = _dipki.CMS_MakeEnvDataFromString(outputfile, inputdata, certlist, None, 0, noptions)
        # Careful: returns +ve number of recipients or a -ve error code
        if (n < 0): raise PKIError(-n)
        return n    # Number of recipients

    @staticmethod
    def read_envdata_to_file(outputfile, inputfile, prikeystr, certfile="", bigfile=False):
        """Read and decrypt CMS enveloped-data object using the recipient's private key.
        file --> file
        """
        noptions = (Cms._BIGFILE if bigfile else 0)
        n = _dipki.CMS_ReadEnvData(outputfile, inputfile, certfile, prikeystr, noptions)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def read_envdata_to_string(inputfile, prikeystr, certfile=""):
        """Read and decrypt CMS enveloped-data object using the recipient's private key.
        file --> string. Assumes output is short ASCII text.
        """
        nc = _dipki.CMS_ReadEnvDataToString(None, 0, inputfile, certfile, prikeystr, 0)
        if (nc < 0): raise PKIError(-nc)
        if (nc == 0): return ""
        buf = create_string_buffer(nc + 1)
        nc = _dipki.CMS_ReadEnvDataToString(buf, nc, inputfile, certfile, prikeystr, 0)
        return str(buf.value)

    @staticmethod
    def make_sigdata(outputfile, inputfile, certlist, prikeystr, hashalg=0, opts=SigDataOpts.DEFAULT, bigfile=False):
        """Create a CMS signed-data object from a data file using user's private RSA key.
        file --> file
        """
        noptions = opts | hashalg | (Cms._BIGFILE if bigfile else 0)
        n = _dipki.CMS_MakeSigData(outputfile, inputfile, certlist, prikeystr, noptions)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def make_sigdata_from_string(outputfile, inputdata, certlist, prikeystr, hashalg=0, opts=SigDataOpts.DEFAULT):
        """Create a CMS signed-data object from a data file using user's private RSA key.
        string --> file
        """
        noptions = opts | hashalg
        n = _dipki.CMS_MakeSigDataFromString(outputfile, inputdata, certlist, prikeystr, noptions)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def make_sigdata_from_sigvalue(outputfile, sigvalue, data, certlist, hashalg=0, opts=SigDataOpts.DEFAULT):
        """Create a CMS object of type SignedData using a pre-computed signature value.
        bytes --> file
        """
        noptions = opts | hashalg
        n = _dipki.CMS_MakeSigDataFromSigValue(outputfile, bytes(sigvalue), len(sigvalue), bytes(data), len(data), certlist, noptions)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def make_detached_sig(outputfile, hexdigest, certlist, prikeystr, hashalg=0, opts=SigDataOpts.DEFAULT):
        """Create a "detached signature" CMS signed-data object from a message digest of the content.
        hexdigest --> file
        """
        noptions = opts | hashalg
        n = _dipki.CMS_MakeDetachedSig(outputfile, hexdigest, certlist, prikeystr, noptions)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def read_sigdata_to_file(outputfile, inputfile, bigfile=False):
        """Read the content from a CMS signed-data object file.
        file --> file
        """
        noptions = (Cms._BIGFILE if bigfile else 0)
        n = _dipki.CMS_ReadSigData(outputfile, inputfile, noptions)
        if (n < 0): raise PKIError(-n)
        return 0

    @staticmethod
    def read_sigdata_to_string(inputfile):
        """Read the content from a CMS signed-data object file directly into a string.
        file --> string. Expects output to be ASCII text.
        """
        nc = _dipki.CMS_ReadSigDataToString(None, 0, inputfile, 0)
        if (nc < 0): raise PKIError(-nc)
        if (nc == 0): return ""
        buf = create_string_buffer(nc + 1)
        nc = _dipki.CMS_ReadSigDataToString(buf, nc, inputfile, 0)
        return str(buf.value)

    @staticmethod
    def verify_sigdata(sigdatafile, certfile="", hexdigest="", bigfile=False):
        """Verify the signature and content of a signed-data CMS object file."""
        noptions = (Cms._BIGFILE if bigfile else 0)
        n = _dipki.CMS_VerifySigData(sigdatafile, certfile, hexdigest, noptions)
        # Catch straightforward invalid signature error
        _DECRYPT_ERROR = -15
        if (n == _DECRYPT_ERROR): return False
        # Raise error for other errors (bad params, missing file, etc)
        if (n < 0): raise PKIError(-n)
        return True

    @staticmethod
    def query_sigdata(cmsfile, query):
        """Query a CMS signed-data object file for selected information. May return an integer or a string."""
        _QUERY_GETTYPE = 0x100000
        _QUERY_STRING = 2
        # Find what type of result to expect: number or string (or error)
        n = _dipki.CMS_QuerySigData(None, 0, cmsfile, query, _QUERY_GETTYPE)
        if (n < 0): raise PKIError(-n)
        if (_QUERY_STRING == n):
            nc = _dipki.CMS_QuerySigData(None, 0, cmsfile, query, 0)
            if (nc < 0): raise PKIError(-nc)
            buf = create_string_buffer(nc + 1)
            nc = _dipki.CMS_QuerySigData(buf, nc, cmsfile, query, 0)
            return str(buf.value)
        else:
            n = _dipki.CMS_QuerySigData(None, 0, cmsfile, query, 0)
            return n

    @staticmethod
    def query_envdata(cmsfile, query):
        """Query a CMS enveloped-data object file for selected information. May return an integer or a string."""
        _QUERY_GETTYPE = 0x100000
        _QUERY_STRING = 2
        # Find what type of result to expect: number or string (or error)
        n = _dipki.CMS_QueryEnvData(None, 0, cmsfile, query, _QUERY_GETTYPE)
        if (n < 0): raise PKIError(-n)
        if (_QUERY_STRING == n):
            nc = _dipki.CMS_QueryEnvData(None, 0, cmsfile, query, 0)
            if (nc < 0): raise PKIError(-nc)
            buf = create_string_buffer(nc + 1)
            nc = _dipki.CMS_QueryEnvData(buf, nc, cmsfile, query, 0)
            return str(buf.value)
        else:
            n = _dipki.CMS_QueryEnvData(None, 0, cmsfile, query, 0)
            return n

    @staticmethod
    def make_comprdata(outputfile, inputfile):
        """Create a new CMS compressed-data file (.p7z) from an existing input file.
        file --> file
        """
        n = _dipki.CMS_MakeComprData(outputfile, inputfile, 0)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def read_comprdata(outputfile, inputfile, opts=ComprDataOpts.DEFAULT):
        """Read and extract the decompressed contents of a CMS compressed-data file.
        file --> file
        """
        n = _dipki.CMS_ReadComprData(outputfile, inputfile, opts)
        if (n < 0): raise PKIError(-n)
        return n


class Cnv:
    """Character conversion routines."""

    # CONSTANTS
    class EndianNess:
        """Byte order."""
        BIG_ENDIAN    = 0x0  #: Big-endian order (default)
        LITTLE_ENDIAN = 0x1  #: Little-endian order

    @staticmethod
    def tohex(data):
        """
        Encode binary data as a hexadecimal string.
        Letters [A-F] are in uppercase. Use `s.lower()` for lowercase.
        """
        nbytes = len(data)
        if (nbytes == 0): return ""
        nc = _dipki.CNV_HexStrFromBytes(None, 0, bytes(data), nbytes)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.CNV_HexStrFromBytes(buf, nc, bytes(data), nbytes)
        return str(buf.value)[:nc]

    @staticmethod
    def fromhex(s):
        """Decode a hexadecimal-encoded string into a byte array."""
        n = _dipki.CNV_BytesFromHexStr(None, 0, s)
        if (n < 0): raise PKIError(-n)
        if (n == 0): return bytes("")
        buf = create_string_buffer(n)
        n = _dipki.CNV_BytesFromHexStr(buf, n, s)
        return bytes(buf.raw)[:n]

    @staticmethod
    def tobase64(data):
        """Encode binary data as a base64 string."""
        nbytes = len(data)
        if (nbytes == 0): return ""
        nc = _dipki.CNV_B64StrFromBytes(None, 0, bytes(data), nbytes)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.CNV_B64StrFromBytes(buf, nc, bytes(data), nbytes)
        return str(buf.value)[:nc]

    @staticmethod
    def frombase64(s):
        """Decode a base64-encoded string into a byte array."""
        n = _dipki.CNV_BytesFromB64Str(None, 0, s)
        if (n < 0): raise PKIError(-n)
        if (n == 0): return bytes("")
        buf = create_string_buffer(n)
        n = _dipki.CNV_BytesFromB64Str(buf, n, s)
        return bytes(buf.raw)[:n]

    @staticmethod
    def tobase58(data):
        """Encode binary data as a base58 string."""
        nbytes = len(data)
        if (nbytes == 0): return ""
        nc = _dipki.CNV_Base58FromBytes(None, 0, bytes(data), nbytes)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.CNV_Base58FromBytes(buf, nc, bytes(data), nbytes)
        return str(buf.value)[:nc]

    @staticmethod
    def frombase58(s):
        """Decode a base58-encoded string into a byte array."""
        n = _dipki.CNV_Base58ToBytes(None, 0, s)
        if (n < 0): raise PKIError(-n)
        if (n == 0): return bytes("")
        buf = create_string_buffer(n)
        n = _dipki.CNV_Base58ToBytes(buf, n, s)
        return bytes(buf.raw)[:n]

    @staticmethod
    def reverse_bytes(data):
        """Reverse the order of a byte array."""
        n = len(data)
        buf = create_string_buffer(n)
        n = _dipki.CNV_ReverseBytes(buf, data, n)
        return bytes(buf.raw)

    @staticmethod
    def num_from_bytes(data, endn=EndianNess.BIG_ENDIAN):
        """Convert the leftmost four bytes of an array to a 32-bit integer."""
        n = _dipki.CNV_NumFromBytes(data, len(data), endn)
        # Force number to be a positive 32-bit integer
        return n & 0xFFFFFFFF

    @staticmethod
    def num_to_bytes(num, endn=EndianNess.BIG_ENDIAN):
        """Convert a 32-bit integer to an array of 4 bytes."""
        n = 4
        buf = create_string_buffer(n)
        n = _dipki.CNV_NumToBytes(buf, n, (num & 0xFFFFFFFF), endn)
        return bytes(buf.raw)

    # UTF-8 STUFF...
    @staticmethod
    def utf8_check(data):
        """Check if a byte array or string contains valid UTF-8 characters. Returns integer code."""
        n = _dipki.CNV_CheckUTF8Bytes(data, len(data))
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def utf8_check_file(filename):
        """Check if a file contains valid UTF-8 characters. Returns integer code."""
        n = _dipki.CNV_CheckUTF8File(filename)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def utf8_check_to_string(n):
        """Return a string describing a code returned by ``utf8_check()`` and ``utf8_check_file()``."""
        d = {
            0: 'Not valid UTF-8',
            1: 'Valid UTF-8, all chars are 7-bit ASCII',
            2: 'Valid UTF-8, contains at least one multi-byte character equivalent to 8-bit ANSI',
            3: 'Valid UTF-8, contains at least one multi-byte character that cannot be represented in a single-byte character set'
        }
        if not n in d: raise PKIError('Invalid code')
        return d[n]

    @staticmethod
    def utf8_to_latin1(b):
        """Convert UTF-8 encoded array of bytes into a Latin-1 string, if possible."""
        n = _dipki.CNV_Latin1FromUTF8Bytes(None, 0, b, len(b))
        if (n < 0): raise PKIError(-n)
        if (n == 0): return ""
        buf = create_string_buffer(n)
        n = _dipki.CNV_Latin1FromUTF8Bytes(buf, n, b, len(b))
        return str(buf.value)

    @staticmethod
    def utf8_from_latin1(s):
        """Convert a string of 8-bit Latin-1 characters into a UTF-8 encoded array of bytes."""
        n = _dipki.CNV_UTF8BytesFromLatin1(None, 0, s)
        if (n < 0): raise PKIError(-n)
        if (n == 0): return bytes("")
        buf = create_string_buffer(n)
        n = _dipki.CNV_UTF8BytesFromLatin1(buf, n, s)
        if (n <= 0): return bytes("")
        return bytes(buf.raw)


class Ecc:
    """Manage keys for elliptic curve cryptography."""

    class CurveName:
        """Supported curve names."""
        SECP192R1 = "secp192r1"    #: P-192
        SECP224R1 = "secp224r1"    #: P-224
        SECP256R1 = "secp256r1"    #: P-256
        SECP384R1 = "secp384r1"    #: P-384
        SECP521R1 = "secp521r1"    #: P-521
        SECP256K1 = "secp256k1"    #: "Bitcoin" curve
        # Alternative synonyms
        P_192 = "P-192"     #: secp192r1
        P_224 = "P-224"     #: secp224r1
        P_256 = "P-256"     #: secp256r1
        P_384 = "P-384"     #: secp384r1
        P_521 = "P-521"     #: secp521r1
        # Yet more alternatives
        PRIME192V1 = "prime192v1"   #: P-192
        PRIME256V1 = "prime256v1"   #: P-256

    class PbeScheme:
        """Password-based encryption scheme to encrypt the private key file."""
        DEFAULT = 0    #: ``pbeWithSHAAnd3-KeyTripleDES-CBC`` from PKCS#12
        PBKDF2_DESEDE3 = 0x1010  #: PBKDF2 using ``des-EDE3-CBC``
        PBKDF2_AES128  = 0x1020  #: PBKDF2 using ``aes128-CBC``
        PBKDF2_AES192  = 0x1030  #: PBKDF2 using ``aes192-CBC``
        PBKDF2_AES256  = 0x1040  #: PBKDF2 using ``aes256-CBC``

    class KeyType:
        """Key type for unencrypted key file.

        Default is ``SubjectPublicKeyInfo`` for an EC public key or ``ECPrivateKey`` for an EC private key.
        """
        DEFAULT = 0  #: Default type: ``SubjectPublicKeyInfo`` for an EC public key or ``ECPrivateKey`` for an EC private key.
        PKCS8 = 0x40000 #: Save private key in PKCS#8 ``PrivateKeyInfo`` format (ignored for a public key).

    class Format:
        """Format for saved key file."""
        DEFAULT = 0  #: Binary
        BINARY  = 0  #: Binary (default)
        PEM = 0x10000  #: PEM-encoded format

    @staticmethod
    def make_keys(pubkeyfile, prikeyfile, curvename, password, pbes=0, params=None, fileformat=0):
        """Generate a new EC public/private key pair."""
        noptions = pbes | fileformat
        n = _dipki.ECC_MakeKeys(pubkeyfile, prikeyfile, curvename, password, params, noptions)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def read_private_key(keyfileorstr, password=""):
        """Return an internal private key string from a file or string containing an EC private key."""
        nc = _dipki.ECC_ReadPrivateKey(None, 0, keyfileorstr, password, 0)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.ECC_ReadPrivateKey(buf, nc, keyfileorstr, password, 0)
        return str(buf.value)[:nc]

    @staticmethod
    def read_public_key(keyfileorstr):
        """Return an internal public key string from a file or string containing an EC public key."""
        nc = _dipki.ECC_ReadPublicKey(None, 0, keyfileorstr, 0)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.ECC_ReadPublicKey(buf, nc, keyfileorstr, 0)
        return str(buf.value)[:nc]

    @staticmethod
    def read_key_by_curve(keyhex, curvename):
        """Return an internal key string of an EC key from its hexadecimal (base16) representation."""
        nc = _dipki.ECC_ReadKeyByCurve(None, 0, keyhex, curvename, 0)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.ECC_ReadKeyByCurve(buf, nc, keyhex, curvename, 0)
        return str(buf.value)[:nc]

    @staticmethod
    def query_key(intkeystr, query):
        """Query an EC key string for selected information. May return an integer or a string."""
        _QUERY_GETTYPE = 0x100000
        _QUERY_STRING = 2
        # Find what type of result to expect: number or string (or error)
        n = _dipki.ECC_QueryKey(None, 0, intkeystr, query, _QUERY_GETTYPE)
        if (n < 0): raise PKIError(-n)
        if (_QUERY_STRING == n):
            nc = _dipki.ECC_QueryKey(None, 0, intkeystr, query, 0)
            if (nc < 0): raise PKIError(-nc)
            buf = create_string_buffer(nc + 1)
            nc = _dipki.ECC_QueryKey(buf, nc, intkeystr, query, 0)
            return str(buf.value)
        else:
            n = _dipki.ECC_QueryKey(None, 0, intkeystr, query, 0)
            return n

    @staticmethod
    def save_key(outputfile, intkeystr, keytype=0, fileformat=0):
        """Save an internal EC key string (public or private) to an unencrypted key file."""
        noptions = keytype | fileformat
        n = _dipki.ECC_SaveKey(outputfile, intkeystr, noptions)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def save_enc_key(outputfile, intkeystr, password, pbescheme=0, params=None, fileformat=0):
        """Save an internal EC private key string to an encrypted private key file."""
        noptions = pbescheme | fileformat
        n = _dipki.ECC_SaveEncKey(outputfile, intkeystr, password, params, noptions)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def publickey_from_private(intkeystr):
        """Return an internal EC public key string from an internal EC private key string."""
        nc = _dipki.ECC_PublicKeyFromPrivate(None, 0, intkeystr, 0)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.ECC_PublicKeyFromPrivate(buf, nc, intkeystr, 0)
        return str(buf.value)[:nc]


class Gen:
    """General info about the core DLL and errors returned by it."""

    @staticmethod
    def version():
        """Return the release version of the core CryptoSys DLL as an integer value."""
        return _dipki.PKI_Version(0, 0)

    @staticmethod
    def compile_time():
        """Return date and time the core CryptoSys DLL was last compiled."""
        nchars = _dipki.PKI_CompileTime(None, 0)
        buf = create_string_buffer(nchars + 1)
        nchars = _dipki.PKI_CompileTime(buf, nchars)
        return str(buf.value)

    @staticmethod
    def module_name():
        """Return full path name of the current process's DLL module."""
        nchars = _dipki.PKI_ModuleName(None, 0, 0)
        buf = create_string_buffer(nchars + 1)
        nchars = _dipki.PKI_ModuleName(buf, nchars, 0)
        return str(buf.value)

    @staticmethod
    def core_platform():
        """Return the platform of the core DLL ('Win32' or 'X64')."""
        nchars = 5
        buf = create_string_buffer(nchars + 1)
        nchars = _dipki.PKI_ModuleName(buf, nchars, 0x40)
        return str(buf.value)[:nchars]

    @staticmethod
    def licence_type():
        """Return licence type: 'D'=Developer 'T'=Trial."""
        n = _dipki.PKI_LicenceType(0)
        return chr(n)

    @staticmethod
    def last_error():
        """Return the last error message set by the toolkit, if any."""
        nchars = _dipki.PKI_LastError(None, 0)
        buf = create_string_buffer(nchars + 1)
        nchars = _dipki.PKI_LastError(buf, nchars)
        return str(buf.value)

    @staticmethod
    def error_lookup(n):
        """Return a description of an error code."""
        nchars = _dipki.PKI_ErrorLookup(None, 0, c_int(n))
        buf = create_string_buffer(nchars + 1)
        nchars = _dipki.PKI_ErrorLookup(buf, nchars, c_int(n))
        return str(buf.value)

    @staticmethod
    def error_code():
        """Return the error code of the _first_ error that occurred when calling the last function."""
        return _dipki.PKI_ErrorCode()


class Hash:
    """Compute message digest hash values."""

    # CONSTANTS
    class Alg:
        """Hash algorithms."""
        SHA1   = 0  #: SHA-1 (default)
        SHA224 = 6  #: SHA-224
        SHA256 = 3  #: SHA-256
        SHA384 = 4  #: SHA-384
        SHA512 = 5  #: SHA-512
        MD5    = 1  #: MD5 (as per RFC 1321)
        RMD160 = 7  #: RIPEMD-160
        BTC160 = 8  #: RIPEMD-160 hash of a SHA-256 hash (``RIPEMD160(SHA256(m))``)

    @staticmethod
    def data(data, alg=Alg.SHA1):
        """Create a message digest hash as a byte array from byte (or string) data."""
        n = _dipki.HASH_Bytes(None, 0, bytes(data), len(data), alg)
        if (n < 0): raise PKIError(-n)
        buf = create_string_buffer(n)
        n = _dipki.HASH_Bytes(buf, n, bytes(data), len(data), alg)
        return bytearray(buf.raw)

    @staticmethod
    def file(filename, alg=Alg.SHA1):
        """Create a message digest hash as a byte array from data in a file."""
        n = _dipki.HASH_File(None, 0, filename, alg)
        if (n < 0): raise PKIError(-n)
        buf = create_string_buffer(n)
        n = _dipki.HASH_File(buf, n, filename, alg)
        return bytearray(buf.raw)

    @staticmethod
    def hex_from_data(data, alg=Alg.SHA1):
        """Create a message digest hash in hexadecimal format from byte (or string) data."""
        nc = _dipki.HASH_HexFromBytes(None, 0, bytes(data), len(data), alg)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.HASH_HexFromBytes(buf, nc, bytes(data), len(data), alg)
        return str(buf.value)

    @staticmethod
    def hex_from_file(filename, alg=Alg.SHA1):
        """Create a message digest hash in hexadecimal format from data in a file."""
        nc = _dipki.HASH_HexFromFile(None, 0, filename, alg)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.HASH_HexFromFile(buf, nc, filename, alg)
        return str(buf.value)

    @staticmethod
    def hex_from_hex(datahex, alg=Alg.SHA1):
        """Create a message digest hash in hexadecimal format from data in a hexadecimal-encoded string."""
        nc = _dipki.HASH_HexFromHex(None, 0, datahex, alg)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.HASH_HexFromHex(buf, nc, datahex, alg)
        return str(buf.value)

    @staticmethod
    def double(data, alg=Alg.SHA1):
        """Create a double hash - hash of hash - as a byte array from byte (or string) data."""
        _HASH_DOUBLE = 0x20000
        n = _dipki.HASH_Bytes(None, 0, bytes(data), len(data), alg | _HASH_DOUBLE)
        if (n < 0): raise PKIError(-n)
        buf = create_string_buffer(n)
        n = _dipki.HASH_Bytes(buf, n, bytes(data), len(data), alg | _HASH_DOUBLE)
        return bytearray(buf.raw)


class Hmac:
    """Compute keyed-hash based message authentication code (HMAC) values."""

    # CONSTANTS
    class Alg:
        """HMAC algorithms."""
        SHA1   = 0  #: HMAC-SHA-1 (default)
        SHA224 = 6  #: HMAC-SHA-224
        SHA256 = 3  #: HMAC-SHA-256
        SHA384 = 4  #: HMAC-SHA-384
        SHA512 = 5  #: HMAC-SHA-512
        MD5    = 1  #: HMAC-MD5

    @staticmethod
    def data(data, key, alg=Alg.SHA1):
        """Create a keyed-hash based message authentication code (HMAC) as a byte array from byte data."""
        n = _dipki.HMAC_Bytes(None, 0, bytes(data), len(data), bytes(key), len(key), alg)
        if (n < 0): raise PKIError(-n)
        buf = create_string_buffer(n)
        n = _dipki.HMAC_Bytes(buf, n, bytes(data), len(data), bytes(key), len(key), alg)
        return bytearray(buf.raw)

    @staticmethod
    def hex_from_data(data, key, alg=Alg.SHA1):
        """Create a keyed-hash based message authentication code (HMAC) in hexadecimal format from byte (or string) data."""
        nc = _dipki.HMAC_HexFromBytes(None, 0, bytes(data), len(data), bytes(key), len(key), alg)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.HMAC_HexFromBytes(buf, nc, bytes(data), len(data), bytes(key), len(key), alg)
        return str(buf.value)

    @staticmethod
    def hex_from_hex(datahex, keyhex, alg=Alg.SHA1):
        """Create a keyed-hash based message authentication code (HMAC) in hexadecimal format from data in hexadecimal-encoded strings."""
        nc = _dipki.HMAC_HexFromHex(None, 0, datahex, keyhex, alg)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.HMAC_HexFromHex(buf, nc, datahex, keyhex, alg)
        return str(buf.value)


class Ocsp:
    """Online Certificate Status Protocol (OCSP) routines."""

    class HashAlg:
        """Hash algorithms."""
        SHA1   = 0  #: SHA-1 (default)
        SHA224 = 6  #: SHA-224
        SHA256 = 3  #: SHA-256
        SHA384 = 4  #: SHA-384
        SHA512 = 5  #: SHA-512
        MD5    = 1  #: MD5 (as per RFC 1321)

    @staticmethod
    def make_request(issuercert, certfile_or_serialnumber, hashalg=0):
        """Create an Online Certification Status Protocol (OCSP) request as a base64 string."""
        nc = _dipki.OCSP_MakeRequest(None, 0, issuercert, certfile_or_serialnumber, "", hashalg)
        if (nc < 0): raise PKIError(-nc)
        if (nc == 0): return ""
        buf = create_string_buffer(nc + 1)
        nc = _dipki.OCSP_MakeRequest(buf, nc, issuercert, certfile_or_serialnumber, "", hashalg)
        return str(buf.value)

    @staticmethod
    def read_response(responsefile, issuercert=""):
        """Read a response to an Online Certification Status Protocol (OCSP) request and outputs the main results in text form."""
        nc = _dipki.OCSP_ReadResponse(None, 0, responsefile, issuercert, "", 0)
        if (nc < 0): raise PKIError(-nc)
        if (nc == 0): return ""
        buf = create_string_buffer(nc + 1)
        nc = _dipki.OCSP_ReadResponse(buf, nc, responsefile, issuercert, "", 0)
        return str(buf.value)


class Pbe:
    """Password-based encryption."""

    class PrfAlg:
        """PRF algorithms."""
        HMAC_SHA1   = 0  #: HMAC-SHA-1 (default)
        HMAC_SHA224 = 6  #: HMAC-SHA-224
        HMAC_SHA256 = 3  #: HMAC-SHA-256
        HMAC_SHA384 = 4  #: HMAC-SHA-384
        HMAC_SHA512 = 5  #: HMAC-SHA-512

    @staticmethod
    def kdf2(dklen, password, salt, count, prfalg=0):
        """Derive a key of any length from a password using the PBKDF2 algorithm."""
        if (dklen <= 0 or dklen > _INTMAX): raise PKIError('dklen out of range')
        buf = create_string_buffer(dklen)
        n = _dipki.PBE_Kdf2(buf, dklen, bytes(password), len(password), bytes(salt), len(salt), count, prfalg)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return bytes(buf.raw)


class Pem:
    """PEM file conversion routines."""

    class EOL:
        DEFAULT = 0  #: Windows CR-LF line endings (default)
        WINDOWS = 0  #: Windows CR-LF line endings
        UNIX = 0x20000  #: Unix/SSL LF line endings

    @staticmethod
    def from_binfile(outputfile, filein, header, linelen=64, eol=0):
        """Create a PEM file from a binary file."""
        n = _dipki.PEM_FileFromBinFileEx(outputfile, filein, header, linelen, eol)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def to_binfile(outputfile, filein):
        """Convert the contents of a PEM file into a binary file."""
        n = _dipki.PEM_FileToBinFile(outputfile, filein)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n


class Pfx:
    """PKCS-12 (PFX) file utilties."""

    class Opts:
        """Bitwise options for creating a PFX file."""
        PLAIN_CERT = 0x2000000  #: Store the certificate in unencrypted form (default is encrypted with 40-bit RC2) 
        CLONE_KEY  = 0x4000000  #: Store the private key in the exact form of the pkcs-8 input file (default is to re-encrypt with Triple DES)
        ALT_FORMAT =  0x100000  #: Create a PFX file with the exact peculiarities used by Microsoft (default is OpenSSL) 
        FORMAT_PEM =   0x10000  #: Create the output file in PEM format (default is DER-encoded binary) 

    @staticmethod
    def make_file(outputfile, certlist, prikeyfile="", password="", friendlyname="", opts=0):
        """Create a PFX (PKCS-12) file from an X.509 certificate and (optional) encrypted private key file."""
        n = _dipki.PFX_MakeFile(outputfile, certlist, prikeyfile, password, friendlyname, opts)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def sig_is_valid(pfxfile, password):
        """Determine if the signature is valid in a pkcs-12 file."""
        _INVALID   = -1
        n = _dipki.PFX_VerifySig(pfxfile, password, 0)
        if (0 == n):
            isvalid = True
        elif (_INVALID == n):
            isvalid = False
        else:
            raise PKIError(-n if n < 0 else n)
        return isvalid


class Pwd:
    """Password dialog utility."""

    @staticmethod
    def prompt(caption="", prompt=""):
        """Return a password entered into a dialog box or empty string if user cancels."""
        _MAXPWDLEN = 512
        nc = _MAXPWDLEN
        buf = create_string_buffer(nc + 1)
        n = _dipki.PWD_PromptEx(buf, nc, caption, prompt, 0)
        if (n <= 0):
            return ""
        return str(buf.value)


class Rng:
    """Random Number Generator to NIST SP800-90."""
    # FIELDS
    SEED_BYTES = 64

    @staticmethod
    def bytes(n):
        """Generate an array of n random bytes."""
        if (n < 0 or n > _INTMAX): raise PKIError('invalid n')
        buf = create_string_buffer(n)
        n = _dipki.RNG_Bytes(buf, n, None, 0)
        return bytes(buf.raw)

    @staticmethod
    def number(lower, upper):
        """Generate a random integer in a given range."""
        if (lower < _INTMIN) or (lower > _INTMAX): raise PKIError('out of range')
        if (upper < _INTMIN) or (upper > _INTMAX): raise PKIError('out of range')
        n = _dipki.RNG_Number(lower, upper)
        return n

    @staticmethod
    def octet():
        """Generate a single random byte."""
        n = _dipki.RNG_Number(0, 255)
        return n

    @staticmethod
    def initialize(seedfilename):
        """Initialize the RNG generator with a seed file."""
        n = _dipki.RNG_Initialize(seedfilename, 0)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def update_seedfile(seedfilename):
        """Update the RNG seed file with more entropy."""
        n = _dipki.RNG_UpdateSeedFile(seedfilename, 0)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n


class Rsa:
    """RSA encryption and key management."""
    # CONSTANTS
    class PbeScheme:
        """Password-based encryption scheme to encrypt the private key file."""
        DEFAULT = 0    #: ``pbeWithSHAAnd3-KeyTripleDES-CBC`` from PKCS#12
        PBKDF2_DESEDE3 = 0x1010  #: PBKDF2 using ``des-EDE3-CBC``
        PBKDF2_AES128  = 0x1020  #: PBKDF2 using ``aes128-CBC``
        PBKDF2_AES192  = 0x1030  #: PBKDF2 using ``aes192-CBC``
        PBKDF2_AES256  = 0x1040  #: PBKDF2 using ``aes256-CBC``

    class PublicExponent:
        """Choice for public exponent (e)."""
        RSAEXP_EQ_3     = 0  #: Set exponent equal to 3 (F0) 
        RSAEXP_EQ_5     = 1  #: Set exponent equal to 5 (F1)
        RSAEXP_EQ_17    = 2  #: Set exponent equal to 17 (F2)
        RSAEXP_EQ_257   = 3  #: Set exponent equal to 257 (F3)
        RSAEXP_EQ_65537 = 4  #: Set exponent equal to 65537 (F4)

    class Format:
        """Format for saved RSA key."""
        DEFAULT = 0  #: Default
        BINARY  = 0  #: Binary DER-encoded (default)
        PEM = 0x10000  #: PEM-encoded
        SSL = 0x20000  #: PEM-encoded compatible with OpenSSL

    class XmlOptions:
        """Bitwise flags when converting between RSA key and XML."""
        RSAKEYVALUE = 0x0001  #: Create in .NET-compatible RSAKeyValue format 
        EXCLPRIVATE = 0x0010  #: Exclude private key even if present
        REQPRIVATE  = 0x0020  #: Require the private key to exist in the XML input or fail
        HEXBINARY   = 0x0100  #: Create in non-standard hex format

    class HashAlg:
        """Hash algorithms."""
        SHA1   = 0  #: SHA-1 (default)
        SHA224 = 6  #: SHA-224
        SHA256 = 3  #: SHA-256
        SHA384 = 4  #: SHA-384
        SHA512 = 5  #: SHA-512
        MD5    = 1  #: MD5 (as per RFC 1321)

    class EME:
        """Encoding method for encryption."""
        PKCSV1_5  = 0x00  #: EME-PKCS1-v1_5 encoding method (default)
        OAEP = 0x10  #: EME-OAEP encoding method 

    @staticmethod
    def make_keys(pubkeyfile, prikeyfile, nbits, exponent, password, pbes=0, params=None, fileformat=0):
        """Generate a new RSA public/private key pair."""
        # TODO: params - not yet available. In a future version
        _NTESTS = 80
        _COUNT = 2048
        noptions = pbes | fileformat
        n = _dipki.RSA_MakeKeys(str(pubkeyfile), str(prikeyfile), nbits, exponent, _NTESTS, _COUNT, password, None, 0, noptions)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def key_bits(keystr):
        """Return number of significant bits in RSA key modulus."""
        n = _dipki.RSA_KeyBits(keystr)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def key_bytes(keystr):
        """Return number of bytes (octets) in RSA key modulus."""
        n = _dipki.RSA_KeyBytes(keystr)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def key_hashcode(keystr):
        """Return the hash code of an internal RSA public or private key string."""
        n = _dipki.RSA_KeyHashCode(keystr)
        if (n == 0): raise PKIError('key_hashcode failed: key string probably invalid')
        # Make sure we format negative values _correctly_ as unsigned
        return format(n & 0xFFFFFFFF, "08X")

    @staticmethod
    def key_isprivate(keystr):
        """Determine if keystring is a private key.
        Return True if the key string contains a valid RSA private key,
        False if a valid RSA public key, or raise PKIError() if invalid.
        """
        n = _dipki.RSA_CheckKey(keystr, 0)
        if (n < 0): raise PKIError(-n)
        return (n == 0)

    @staticmethod
    def key_value(keystr, fieldname):
        """Extract a base64-encoded RSA key value from internal key string."""
        nc = _dipki.RSA_KeyValue(None, 0, keystr, fieldname, 0)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.RSA_KeyValue(buf, nc, keystr, fieldname, 0)
        return str(buf.value)

    @staticmethod
    def key_match(prikeystr, pubkeystr):
        """Determine if a pair of "internal" RSA private and public key strings are matched.
        Return True if the keystrings are valid and matched,
        False if the keystrings are valid but not matched, or raise PKIError().
        """
        _NO_MATCH_ERROR = -21
        n = _dipki.RSA_KeyMatch(prikeystr, pubkeystr)
        if (n == 0):
            return True
        elif (n == _NO_MATCH_ERROR):
            return False
        else:
            raise PKIError(-n if n < 0 else n)

    @staticmethod
    def publickey_from_private(intkeystr):
        """Return an internal RSA public key string from an internal RSA private key string."""
        nc = _dipki.RSA_PublicKeyFromPrivate(None, 0, intkeystr, 0)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.RSA_PublicKeyFromPrivate(buf, nc, intkeystr, 0)
        return str(buf.value)[:nc]

    @staticmethod
    def to_xmlstring(keystr, opts=0):
        """Return an XML string representation of an RSA internal key string."""
        nc = _dipki.RSA_ToXMLString(None, 0, keystr, opts)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.RSA_ToXMLString(buf, nc, keystr, opts)
        return str(buf.value)[:nc]

    @staticmethod
    def from_xmlstring(xmlstr, opts=0):
        """Return an RSA key string in internal format from an XML string."""
        nc = _dipki.RSA_FromXMLString(None, 0, xmlstr, opts)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.RSA_FromXMLString(buf, nc, xmlstr, opts)
        return str(buf.value)[:nc]

    @staticmethod
    def read_private_key(keyfileorstr, password=""):
        """Return an internal private key string from a file or string containing an RSA private key."""
        nc = _dipki.RSA_ReadAnyPrivateKey(None, 0, keyfileorstr, password, 0)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.RSA_ReadAnyPrivateKey(buf, nc, keyfileorstr, password, 0)
        return str(buf.value)[:nc]

    @staticmethod
    def read_public_key(keyfileorstr):
        """Return an internal public key string from a file or string containing an RSA public key."""
        nc = _dipki.RSA_ReadAnyPublicKey(None, 0, keyfileorstr, 0)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.RSA_ReadAnyPublicKey(buf, nc, keyfileorstr, 0)
        return str(buf.value)[:nc]

    @staticmethod
    def save_key(outputfile, keystr, fileformat=0):
        """Save an internal RSA key string (public or private) to an unencrypted key file."""
        # TODO: at some stage add this to core C library. For now we do in parts.
        if (Rsa.key_isprivate(keystr)):
            n = _dipki.RSA_SavePrivateKeyInfo(outputfile, keystr, fileformat)
        else:
            n = _dipki.RSA_SavePublicKey(outputfile, keystr, fileformat)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def save_enc_key(outputfile, intkeystr, password, pbescheme=0, count=2048, params=None, fileformat=0):
        """Save an internal RSA private key string to an encrypted private key file."""
        # TODO: add params in a future version (when available) and deprecate count
        noptions = pbescheme | fileformat
        n = _dipki.RSA_SaveEncPrivateKey(outputfile, intkeystr, count, password, noptions)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def raw_private(block, prikeystr):
        """Return RSA transformation of block using private key."""
        nd = len(block)
        buf = create_string_buffer(block, nd)
        n = _dipki.RSA_RawPrivate(buf, nd, prikeystr, 0)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return bytes(buf.raw)

    @staticmethod
    def raw_public(block, pubkeystr):
        """return RSA transformation of block using public key."""
        nd = len(block)
        buf = create_string_buffer(block, nd)
        n = _dipki.RSA_RawPublic(buf, nd, pubkeystr, 0)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return bytes(buf.raw)

    @staticmethod
    def encode_msg_for_signature(keybytes, message, hashalg=HashAlg.SHA1, digest_only=False):
        """
        Create an encoded message for signature. EMSA-PKCS1-v1_5 only.
        Default is to pass the entire message-to-be-signed.
        Set `digest_only=True` to pass the digest value only.
        """
        _EMSIG_PKCSV1_5 = 0x20
        _DIGESTONLY = 0x1000
        noptions = _EMSIG_PKCSV1_5 | hashalg
        if digest_only: noptions |= _DIGESTONLY
        n = keybytes
        buf = create_string_buffer(n)
        n = _dipki.RSA_EncodeMsg(buf, n, bytes(message), len(message), noptions)
        if (n < 0): raise PKIError(-n)
        # success == 0
        return bytes(buf.raw)

    @staticmethod
    def decode_digest_for_signature(data, full_digestinfo=False):
        """Extract digest (or digestinfo) from an EMSA-PKCS1-v1_5-encoded block."""
        _EMSIG_PKCSV1_5 = 0x20
        _DIGINFO = 0x2000
        noptions = (_EMSIG_PKCSV1_5 | _DIGINFO) if full_digestinfo else _EMSIG_PKCSV1_5
        n = _dipki.RSA_DecodeMsg(None, 0, bytes(data), len(data), noptions)
        if (n < 0): raise PKIError(-n)
        if (n == 0): return bytes("")
        buf = create_string_buffer(n)
        n = _dipki.RSA_DecodeMsg(buf, n, bytes(data), len(data), noptions)
        return bytes(buf.raw)[:n]

    @staticmethod
    def encode_msg_for_encryption(keybytes, message, method=EME.PKCSV1_5):
        """Create an encoded message for encryption (EME) to PKCS#1."""
        nb = keybytes
        buf = create_string_buffer(nb)
        n = _dipki.RSA_EncodeMsg(buf, nb, bytes(message), len(message), method)
        if (n < 0): raise PKIError(-n)
        # success == 0
        return bytes(buf.raw)

    @staticmethod
    def decode_msg_for_encryption(data, method=EME.PKCSV1_5):
        """Extract message from a PKCS#1 EME-encoded block."""
        n = _dipki.RSA_DecodeMsg(None, 0, bytes(data), len(data), method)
        if (n < 0): raise PKIError(-n)
        if (n == 0): return bytes("")
        buf = create_string_buffer(n)
        n = _dipki.RSA_DecodeMsg(buf, n, bytes(data), len(data), method)
        return bytes(buf.raw)[:n]

    @staticmethod
    def encrypt(data, pubkeystr, method=EME.PKCSV1_5):
        """Encrypt a short message using RSA encryption."""
        blk = Rsa.encode_msg_for_encryption(Rsa.key_bytes(pubkeystr), data, method)
        b = Rsa.raw_public(blk, pubkeystr)
        return b

    @staticmethod
    def decrypt(data, prikeystr, method=EME.PKCSV1_5):
        """Decrypt a message encrypted using RSA encryption."""
        blk = Rsa.raw_private(data, prikeystr)
        b = Rsa.decode_msg_for_encryption(blk, method)
        return b


class Sig:
    """Create and verify digital signatures."""

    class Alg:
        """Signature algorithm to use."""
        DEFAULT = ""  #: Use default signature algorithm [rsa-sha1/sha1WithRSAEncryption] 
        RSA_SHA1 = "sha1WithRSAEncryption"  #: Use sha1WithRSAEncryption (rsa-sha1) signature algorithm 
        RSA_SHA224 = "sha224WithRSAEncryption"  #: Use sha224WithRSAEncryption (rsa-sha224) signature algorithm 
        RSA_SHA256 = "sha256WithRSAEncryption"  #: Use sha256WithRSAEncryption (rsa-sha256) signature algorithm 
        RSA_SHA384 = "sha384WithRSAEncryption"  #: Use sha384WithRSAEncryption (rsa-sha384) signature algorithm 
        RSA_SHA512 = "sha512WithRSAEncryption"  #: Use sha512WithRSAEncryption (rsa-sha512) signature algorithm 
        RSA_MD5 = "md5WithRSAEncryption"  #: Use md5WithRSAEncryption (rsa-md5) signature algorithm (for legacy applications - not recommended for new implementations)
        ECDSA_SHA1 = "ecdsaWithSHA1"      #: Use ecdsaWithSHA1 (ecdsa-sha1) signature algorithm 
        ECDSA_SHA224 = "ecdsaWithSHA224"  #: Use ecdsaWithSHA224 (ecdsa-sha224) signature algorithm 
        ECDSA_SHA256 = "ecdsaWithSHA256"  #: Use ecdsaWithSHA256 (ecdsa-sha256) signature algorithm 
        ECDSA_SHA384 = "ecdsaWithSHA384"  #: Use ecdsaWithSHA384 (ecdsa-sha384) signature algorithm 
        ECDSA_SHA512 = "ecdsaWithSHA512"  #: Use ecdsaWithSHA512 (ecdsa-sha512) signature algorithm 

    class Opts:
        """Options for ECDSA signatures."""
        DEFAULT = 0  #: Default options
        DETERMINISTIC = 0x2000  #: Use the deterministic digital signature generation procedure of [RFC6979] for ECDSA signature [default=random k]
        ASN1DER = 0x200000  #: Form ECDSA signature value as a DER-encoded ASN.1 structure [default= ``r||s``] 

    class Encoding:
        """Encodings for signature output."""
        DEFAULT = 0  #: Default encoding (base64) 
        BASE64 = 0   #: Base64 encoding (default) 
        HEX       = 0x30000  #: Hexadecimal encoding
        BASE64URL = 0x40000  #: URL-safe base64 encoding as in section 5 of [RFC4648]

    @staticmethod
    def sign_data(data, keyfile, password, alg, opts=Opts.DEFAULT, encoding=Encoding.DEFAULT):
        """Compute a signature value over data in a byte array."""
        noptions = int(opts) | int(encoding)
        nc = _dipki.SIG_SignData(None, 0, bytes(data), len(data), keyfile, password, str(alg), noptions)
        if (nc < 0): raise PKIError(-nc)
        if (nc == 0): return ""
        buf = create_string_buffer(nc + 1)
        nc = _dipki.SIG_SignData(buf, nc, bytes(data), len(data), keyfile, password, str(alg), noptions)
        return str(buf.value)

    @staticmethod
    def sign_digest(digest, keyfile, password, alg, opts=Opts.DEFAULT, encoding=Encoding.DEFAULT):
        """Compute a signature value over a message digest value."""
        _USEDIGEST = 0x1000
        noptions = int(opts) | int(encoding) | _USEDIGEST
        nc = _dipki.SIG_SignData(None, 0, bytes(digest), len(digest), keyfile, password, str(alg), noptions)
        if (nc < 0): raise PKIError(-nc)
        if (nc == 0): return ""
        buf = create_string_buffer(nc + 1)
        nc = _dipki.SIG_SignData(buf, nc, bytes(digest), len(digest), keyfile, password, str(alg), noptions)
        return str(buf.value)

    @staticmethod
    def sign_file(datafile, keyfile, password, alg, opts=Opts.DEFAULT, encoding=Encoding.DEFAULT):
        """Compute a signature value over binary data in a file."""
        noptions = int(opts) | int(encoding)
        nc = _dipki.SIG_SignFile(None, 0, datafile, keyfile, password, str(alg), noptions)
        if (nc < 0): raise PKIError(-nc)
        if (nc == 0): return ""
        buf = create_string_buffer(nc + 1)
        nc = _dipki.SIG_SignFile(buf, nc, datafile, keyfile, password, str(alg), noptions)
        return str(buf.value)

    @staticmethod
    def data_is_verified(sig, data, certorkey, alg):
        """Verify a signature value over data in a byte array."""
        n = _dipki.SIG_VerifyData(sig, bytes(data), len(data), certorkey, str(alg), 0)
        # Catch straightforward invalid signature error
        _DECRYPT_ERROR = -15
        if (n == _DECRYPT_ERROR): return False
        # Raise error for other errors (bad params, missing file, etc)
        if (n < 0): raise PKIError(-n)
        return True

    @staticmethod
    def digest_is_verified(sig, digest, certorkey, alg):
        """Verify a signature value over a message digest value of data ."""
        _USEDIGEST = 0x1000
        n = _dipki.SIG_VerifyData(sig, bytes(digest), len(digest), certorkey, str(alg), _USEDIGEST)
        # Catch straightforward invalid signature error
        _DECRYPT_ERROR = -15
        if (n == _DECRYPT_ERROR): return False
        # Raise error for other errors (bad params, missing file, etc)
        if (n < 0): raise PKIError(-n)
        return True

    @staticmethod
    def file_is_verified(sig, datafile, certorkey, alg):
        """Verify a signature value over data in a file."""
        n = _dipki.SIG_VerifyFile(sig, datafile, certorkey, str(alg), 0)
        # Catch straightforward invalid signature error
        _DECRYPT_ERROR = -15
        if (n == _DECRYPT_ERROR): return False
        # Raise error for other errors (bad params, missing file, etc)
        if (n < 0): raise PKIError(-n)
        return True


class Smime:
    """S/MIME entity utilities."""

    class Opts():
        """Bitwise flags."""
        ENCODE_BASE64 = 0x10000  #: Encode output in base64 
        ENCODE_BINARY = 0x20000  #: Encode body in binary encoding 
        ADDX = 0x100000  #: Add an "x-" to the content subtype (for compatibility with legacy applications) 

    @staticmethod
    def wrap(outputfile, inputfile, opts=0):
        """Wrap a CMS object in an S/MIME entity."""
        n = _dipki.SMIME_Wrap(outputfile, inputfile, "", opts)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def extract(outputfile, inputfile, opts=0):
        """Extract the body from an S/MIME entity."""
        n = _dipki.SMIME_Extract(outputfile, inputfile, opts)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def query(filename, query):
        """Query an S/MIME entity for selected information."""
        nc = _dipki.SMIME_Query(None, 0, filename, query, 0)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.SMIME_Query(buf, nc, filename, query, 0)
        return str(buf.value)


class Wipe:
    """Wipe data securely."""
    @staticmethod
    def file(filename):
        """Securely wipe and delete a file using 7-pass DOD standards."""
        n = _dipki.WIPE_File(filename, 0)
        if (n != 0): raise PKIError(-n if n < 0 else n)

    @staticmethod
    def data(data):
        """Zeroize data in memory."""
        n = _dipki.WIPE_Data(bytes(data), len(data))
        if (n != 0): raise PKIError(-n if n < 0 else n)


class X509:
    """Create and manage X.509 certificates."""
    # CONSTANTS
    class KeyUsageFlags:
        """Bitwise flags for key usage in certificate."""
        NONE = 0    #: None
        DIGITALSIGNATURE  = 0x0001  #: Set the ``digitalSignature`` bit
        NONREPUDIATION    = 0x0002  #: Set the ``nonRepudiation`` (``contentCommitment``) bit
        KEYENCIPHERMENT   = 0x0004  #: Set the ``keyEncipherment`` bit
        DATAENCIPHERMENT  = 0x0008  #: Set the ``dataEncipherment`` bit
        KEYAGREEMENT      = 0x0010  #: Set the ``keyAgreement`` bit
        KEYCERTSIGN       = 0x0020  #: Set the ``keyCertSign`` bit
        CRLSIGN           = 0x0040  #: Set the ``cRLSign`` bit
        ENCIPHERONLY      = 0x0080  #: Set the ``encipherOnly`` bit
        DECIPHERONLY      = 0x0100  #: Set the ``decipherOnly`` bit

    class Opts:
        """
        Various option flags used by some methods of this class.
        Combine using 'bitwise or' operator ``|``.
        Ignored if not applicable for the particular method.
        Check manual for details.
        """
        FORMAT_PEM     = 0x10000  #: Create in PEM-encoded format (default for CSR)
        FORMAT_BIN     = 0x20000  #: Create in binary format (default for X.509 cert and CRL)
        REQ_KLUDGE    = 0x100000  #: Create a request with the "kludge" that omits the strictly mandatory attributes completely [default = include attributes with zero-length field]
        NO_TIMECHECK  = 0x200000  #: Avoid checking if the certificates are valid now (default = check validity dates against system clock)
        LATIN1        = 0x400000  #: Re-encode Unicode or UTF-8 string as Latin-1, if possible 
        UTF8          = 0x800000  #: Encode distinguished name as UTF8String [default = PrintableString] 
        AUTHKEYID    = 0x1000000  #: Add the issuer's KeyIdentifier, if present, as an AuthorityKeyIdentifer [default = do not add] 
        NO_BASIC     = 0x2000000  #: Disable the BasicConstraints extension [default = include] 
        CA_TRUE      = 0x4000000  #: Set the BasicConstraints subject type to be a CA [default = End Entity] 
        VERSION1     = 0x8000000  #: Create a Version 1 certificate, i.e. no extensions [default = Version 3] 
        LDAP            = 0x1000  #: Output distinguished name in LDAP string representation 
        DECIMAL         = 0x8000  #: Output serial number in decimal format [default = hex] 

    class SigAlg:
        """Signature algorithm to use for signatures."""
        SHA1RSA    = 0  #: Sign with sha1WithRSAEncryption (rsa-sha1) (default)
        SHA224RSA  = 6  #: Sign with sha224WithRSAEncryption (rsa-sha224)
        SHA256RSA  = 3  #: Sign with sha256WithRSAEncryption (rsa-sha256)
        SHA384RSA  = 4  #: Sign with sha384WithRSAEncryption (rsa-sha384)
        SHA512RSA  = 5  #: Sign with sha512WithRSAEncryption (rsa-sha512) 
        MD5RSA     = 1  #: Sign with md5WithRSAEncryption (rsa-md5) 

    class HashAlg:
        """Hash algorithms."""
        SHA1   = 0  #: SHA-1 (default)
        SHA224 = 6  #: SHA-224
        SHA256 = 3  #: SHA-256
        SHA384 = 4  #: SHA-384
        SHA512 = 5  #: SHA-512
        MD5    = 1  #: MD5 (as per RFC 1321)

    @staticmethod
    def make_cert(newcertfile, issuercert, subject_pubkeyfile, issuer_prikeyfile, password, certnum, yearsvalid, distname, extns="", keyusage=0, sigalg=0, opts=0):
        """Create an X.509 certificate using subject's public key and issuer's private key."""
        # Note order of params is different from C version (password is not optional)
        n = _dipki.X509_MakeCert(newcertfile, issuercert, subject_pubkeyfile, issuer_prikeyfile, certnum, yearsvalid, distname, extns, keyusage, password, sigalg | opts)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def make_cert_self(newcertfile, prikeyfile, password, certnum, yearsvalid, distname, extns="", keyusage=0, sigalg=0, opts=0):
        """Create a self-signed X.509 certificate."""
        # Note order of params is different from C version (password is not optional)
        n = _dipki.X509_MakeCertSelf(newcertfile, prikeyfile, certnum, yearsvalid, distname, extns, keyusage, password, sigalg | opts)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def cert_request(newcsrfile, prikeyfile, password, distname, extns="", sigalg=0, opts=0):
        """Create a self-signed X.509 certificate."""
        # Note order of params is different from C version (password is not optional)
        n = _dipki.X509_CertRequest(newcsrfile, prikeyfile, distname, extns, password, sigalg | opts)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def make_crl(newcrlfile, issuercert, prikeyfile, password, revokedcertlist="", extns="", sigalg=0, opts=0):
        """Create an X.509 Certificate Revocation List (CRL). Version 1 only."""
        n = _dipki.X509_MakeCRL(newcrlfile, issuercert, prikeyfile, password, revokedcertlist, extns, sigalg | opts)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def text_dump(outputfile, certfile):
        """Dump details of X.509 certificate (or CRL or CSR) to a text file."""
        n = _dipki.X509_TextDump(outputfile, certfile, 0)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def query_cert(filename, query, opts=0):
        """Query an X.509 certificate file for selected information. May return an integer or a string."""
        _QUERY_GETTYPE = 0x100000
        _QUERY_STRING = 2
        # Find what type of result to expect: number or string (or error)
        n = _dipki.X509_QueryCert(None, 0, filename, query, _QUERY_GETTYPE)
        if (n < 0): raise PKIError(-n)
        if (_QUERY_STRING == n):
            nc = _dipki.X509_QueryCert(None, 0, filename, query, opts)
            if (nc < 0): raise PKIError(-nc)
            buf = create_string_buffer(nc + 1)
            nc = _dipki.X509_QueryCert(buf, nc, filename, query, opts)
            return str(buf.value)
        else:
            n = _dipki.X509_QueryCert(None, 0, filename, query, opts)
            return n

    @staticmethod
    def read_string_from_file(certfilename):
        """Create a base64 string representation of an X.509 certificate."""
        nc = _dipki.X509_ReadStringFromFile(None, 0, certfilename, 0)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.X509_ReadStringFromFile(buf, nc, certfilename, 0)
        return str(buf.value)

    @staticmethod
    def save_file_from_string(newcertfile, certstring, fileformat=0):
        """Create an X.509 certificate file from its base64 string representation."""
        n = _dipki.X509_SaveFileFromString(newcertfile, certstring, fileformat)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def key_usage_flags(certfile):
        """Return a bitfield containing the keyUsage flags for an X.509 certificate. See X509.KeyUsageFlags."""
        n = _dipki.X509_KeyUsageFlags(certfile)
        if (n < 0): raise PKIError(-n)
        return n & 0xFFFFFFFF

    @staticmethod
    def cert_thumb(certfilename, hashalg=0):
        """Return the thumbprint (message digest hash) of an X.509 certificate."""
        nc = _dipki.X509_CertThumb(certfilename, None, 0, hashalg)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.X509_CertThumb(certfilename, buf, nc, hashalg)
        return str(buf.value)

    @staticmethod
    def cert_hashissuersn(certfilename, hashalg=0):
        """Return the hash of the issuer and serial number."""
        nc = _dipki.X509_HashIssuerAndSN(certfilename, None, 0, hashalg)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.X509_HashIssuerAndSN(certfilename, buf, nc, hashalg)
        return str(buf.value)

    @staticmethod
    def cert_is_valid_now(certfile):
        """Verify that an X.509 certificate is currently valid as per system clock."""
        # Legacy anomaly with *positive* error code
        _VALID_NOW = 0
        _EXPIRED   = -1
        n = _dipki.X509_CertIsValidNow(certfile, 0)
        if (_VALID_NOW == n):
            isvalid = True
        elif (_EXPIRED == n):
            isvalid = False
        else:
            raise PKIError(-n if n < 0 else n)
        return isvalid

    @staticmethod
    def cert_is_revoked(certfile, crlfile, crl_issuercert="", isodate=""):
        """Check whether an X.509 certificate has been revoked in a given Certificate Revocation List (CRL)."""
        _REVOKED = 1
        n = _dipki.X509_CheckCertInCRL(certfile, crlfile, crl_issuercert, isodate, 0)
        if (n < 0): raise PKIError(-n)
        return (_REVOKED == n)

    @staticmethod
    def cert_is_verified(certfile, issuercert):
        """Verify that an X.509 certificate (or X.509 certificate revocation list (CRL) or PKCS-10 certificate signing request (CSR)) has been signed by its issuer."""
        # Legacy anomaly with *positive* error code
        _SUCCESS = 0
        _FAILURE = -1
        n = _dipki.X509_VerifyCert(certfile, issuercert, 0)
        if (_SUCCESS == n):
            isvalid = True
        elif (_FAILURE == n):
            isvalid = False
        else:
            raise PKIError(-n if n < 0 else n)
        return isvalid

    @staticmethod
    def cert_path_is_valid(certlist, trustedcert="", opts=0):
        """Validate a certificate path."""
        n = _dipki.X509_ValidatePath(certlist, trustedcert, opts)
        # 0 => OK; +1 => path invalid; -ve error code =>some unexpected error
        if (n < 0): raise PKIError(-n)
        return (0 == n)

    @staticmethod
    def get_cert_count_from_p7(p7file, index):
        """Return number of certificates in a PKCS-7 "certs-only" certificate chain file."""
        n = _dipki.X509_GetCertFromP7Chain(None, p7file, index, 0)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def get_cert_from_p7(outfile, p7file, index):
        """Extract an X.509 certificate from a PKCS-7 "certs-only" certificate chain file, saving the output directly as a new file."""
        if (index <= 0): raise PKIError("Invalid index: " + str(index))
        n = _dipki.X509_GetCertFromP7Chain(outfile, p7file, index, 0)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def get_cert_from_pfx(outfile, pfxfile, password, noptions=0):
        """Extract an X.509 certificate from a PKCS-12 PFX/.p12 file, saving the output directly as a new file."""
        n = _dipki.X509_GetCertFromPFX(outfile, pfxfile, password, noptions)
        if (n < 0): raise PKIError(-n)
        return n


class _NotUsed:
    """Dummy for parsing."""
    pass


# PROTOTYPES (derived from diCrPKI.h v11.1.0)
# If wrong argument type is passed, these will raise an `ArgumentError` exception
#     ArgumentError: argument 1: <type 'exceptions.TypeError'>: wrong type
_dipki.PKI_Version.argtypes = [c_void_p, c_void_p]
_dipki.PKI_LicenceType.argtypes = [c_int]
_dipki.PKI_LastError.argtypes = [c_char_p, c_int]
_dipki.PKI_ErrorCode.argtypes = []
_dipki.PKI_ErrorLookup.argtypes = [c_char_p, c_int, c_int]
_dipki.PKI_CompileTime.argtypes = [c_char_p, c_int]
_dipki.PKI_ModuleName.argtypes = [c_char_p, c_int, c_int]
_dipki.PKI_PowerUpTests.argtypes = [c_int]
_dipki.CMS_MakeEnvData.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int, c_int]
_dipki.CMS_MakeEnvDataFromString.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int, c_int]
_dipki.CMS_ReadEnvData.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.CMS_ReadEnvDataToString.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_char_p, c_int]
_dipki.CMS_MakeSigData.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.CMS_MakeSigDataFromString.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.CMS_MakeSigDataFromSigValue.argtypes = [c_char_p, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int]
_dipki.CMS_MakeDetachedSig.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.CMS_ReadSigData.argtypes = [c_char_p, c_char_p, c_int]
_dipki.CMS_ReadSigDataToString.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.CMS_GetSigDataDigest.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.CMS_VerifySigData.argtypes = [c_char_p, c_char_p, c_char_p, c_int]
_dipki.CMS_QuerySigData.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.CMS_QueryEnvData.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.CMS_MakeComprData.argtypes = [c_char_p, c_char_p, c_int]
_dipki.CMS_ReadComprData.argtypes = [c_char_p, c_char_p, c_int]
_dipki.RSA_MakeKeys.argtypes = [c_char_p, c_char_p, c_int, c_int, c_int, c_int, c_char_p, c_void_p, c_int, c_int]
_dipki.RSA_ReadEncPrivateKey.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.RSA_ReadPrivateKeyInfo.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.RSA_GetPrivateKeyFromPFX.argtypes = [c_char_p, c_char_p, c_int]
_dipki.RSA_ReadPublicKey.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.RSA_GetPublicKeyFromCert.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.RSA_SavePublicKey.argtypes = [c_char_p, c_char_p, c_int]
_dipki.RSA_SavePrivateKeyInfo.argtypes = [c_char_p, c_char_p, c_int]
_dipki.RSA_SaveEncPrivateKey.argtypes = [c_char_p, c_char_p, c_int, c_char_p, c_int]
_dipki.RSA_KeyBits.argtypes = [c_char_p]
_dipki.RSA_KeyBytes.argtypes = [c_char_p]
_dipki.RSA_ToXMLString.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.RSA_FromXMLString.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.RSA_CheckKey.argtypes = [c_char_p, c_int]
_dipki.RSA_KeyHashCode.argtypes = [c_char_p]
_dipki.RSA_KeyMatch.argtypes = [c_char_p, c_char_p]
_dipki.RSA_ReadPrivateKeyFromPFX.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.RSA_PublicKeyFromPrivate.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.RSA_ReadAnyPrivateKey.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.RSA_ReadAnyPublicKey.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.RSA_KeyValue.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.RSA_RawPublic.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.RSA_RawPrivate.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.RSA_EncodeMsg.argtypes = [c_char_p, c_int, c_char_p, c_int, c_int]
_dipki.RSA_DecodeMsg.argtypes = [c_char_p, c_int, c_char_p, c_int, c_int]
_dipki.ECC_MakeKeys.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.ECC_ReadKeyByCurve.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.ECC_ReadPrivateKey.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.ECC_ReadPublicKey.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.ECC_SaveEncKey.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.ECC_SaveKey.argtypes = [c_char_p, c_char_p, c_int]
_dipki.ECC_PublicKeyFromPrivate.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.ECC_QueryKey.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.PFX_MakeFile.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.PFX_VerifySig.argtypes = [c_char_p, c_char_p, c_int]
_dipki.X509_MakeCert.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int, c_int, c_char_p, c_char_p, c_int, c_char_p, c_int]
_dipki.X509_MakeCertSelf.argtypes = [c_char_p, c_char_p, c_int, c_int, c_char_p, c_char_p, c_int, c_char_p, c_int]
_dipki.X509_CertRequest.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.X509_VerifyCert.argtypes = [c_char_p, c_char_p, c_int]
_dipki.X509_CertThumb.argtypes = [c_char_p, c_char_p, c_int, c_int]
_dipki.X509_CertIsValidNow.argtypes = [c_char_p, c_int]
_dipki.X509_CertIssuedOn.argtypes = [c_char_p, c_char_p, c_int, c_int]
_dipki.X509_CertExpiresOn.argtypes = [c_char_p, c_char_p, c_int, c_int]
_dipki.X509_CertSerialNumber.argtypes = [c_char_p, c_char_p, c_int, c_int]
_dipki.X509_HashIssuerAndSN.argtypes = [c_char_p, c_char_p, c_int, c_int]
_dipki.X509_CertIssuerName.argtypes = [c_char_p, c_char_p, c_int, c_char_p, c_int]
_dipki.X509_CertSubjectName.argtypes = [c_char_p, c_char_p, c_int, c_char_p, c_int]
_dipki.X509_GetCertFromP7Chain.argtypes = [c_char_p, c_char_p, c_int, c_int]
_dipki.X509_GetCertFromPFX.argtypes = [c_char_p, c_char_p, c_char_p, c_int]
_dipki.X509_KeyUsageFlags.argtypes = [c_char_p]
_dipki.X509_QueryCert.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.X509_ReadStringFromFile.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.X509_SaveFileFromString.argtypes = [c_char_p, c_char_p, c_int]
_dipki.X509_TextDump.argtypes = [c_char_p, c_char_p, c_int]
_dipki.X509_ValidatePath.argtypes = [c_char_p, c_char_p, c_int]
_dipki.X509_MakeCRL.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.X509_CheckCertInCRL.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.OCSP_MakeRequest.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_char_p, c_int]
_dipki.OCSP_ReadResponse.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_char_p, c_int]
_dipki.TDEA_HexMode.argtypes = [c_char_p, c_char_p, c_char_p, c_int, c_char_p, c_char_p]
_dipki.TDEA_B64Mode.argtypes = [c_char_p, c_char_p, c_char_p, c_int, c_char_p, c_char_p]
_dipki.TDEA_BytesMode.argtypes = [c_char_p, c_char_p, c_int, c_char_p, c_int, c_char_p, c_char_p]
_dipki.TDEA_File.argtypes = [c_char_p, c_char_p, c_char_p, c_int, c_char_p, c_char_p]
_dipki.CIPHER_Bytes.argtypes = [c_int, c_char_p, c_char_p, c_int, c_char_p, c_char_p, c_char_p, c_int]
_dipki.CIPHER_File.argtypes = [c_int, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.CIPHER_Hex.argtypes = [c_int, c_char_p, c_int, c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.CIPHER_KeyWrap.argtypes = [c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_int]
_dipki.CIPHER_KeyUnwrap.argtypes = [c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_int]
_dipki.CIPHER_EncryptBytesPad.argtypes = [c_char_p, c_int, c_char_p, c_int, c_char_p, c_char_p, c_char_p, c_int]
_dipki.CIPHER_DecryptBytesPad.argtypes = [c_char_p, c_int, c_char_p, c_int, c_char_p, c_char_p, c_char_p, c_int]
_dipki.CIPHER_EncryptBytes2.argtypes = [c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int]
_dipki.CIPHER_DecryptBytes2.argtypes = [c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int]
_dipki.CIPHER_FileEncrypt.argtypes = [c_char_p, c_char_p, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int]
_dipki.CIPHER_FileDecrypt.argtypes = [c_char_p, c_char_p, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int]
_dipki.HASH_Bytes.argtypes = [c_char_p, c_int, c_void_p, c_int, c_int]
_dipki.HASH_File.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.HASH_HexFromBytes.argtypes = [c_char_p, c_int, c_void_p, c_int, c_int]
_dipki.HASH_HexFromFile.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.HASH_HexFromHex.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.HMAC_Bytes.argtypes = [c_char_p, c_int, c_void_p, c_int, c_void_p, c_int, c_int]
_dipki.HMAC_HexFromBytes.argtypes = [c_char_p, c_int, c_void_p, c_int, c_void_p, c_int, c_int]
_dipki.HMAC_HexFromHex.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.CNV_B64StrFromBytes.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.CNV_BytesFromB64Str.argtypes = [c_char_p, c_int, c_char_p]
_dipki.CNV_B64Filter.argtypes = [c_char_p, c_char_p, c_int]
_dipki.CNV_HexStrFromBytes.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.CNV_BytesFromHexStr.argtypes = [c_char_p, c_int, c_char_p]
_dipki.CNV_HexFilter.argtypes = [c_char_p, c_char_p, c_int]
_dipki.CNV_Base58FromBytes.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.CNV_Base58ToBytes.argtypes = [c_char_p, c_int, c_char_p]
_dipki.CNV_UTF8FromLatin1.argtypes = [c_char_p, c_int, c_char_p]
_dipki.CNV_Latin1FromUTF8.argtypes = [c_char_p, c_int, c_char_p]
_dipki.CNV_CheckUTF8.argtypes = [c_char_p]
_dipki.CNV_UTF8BytesFromLatin1.argtypes = [c_char_p, c_int, c_char_p]
_dipki.CNV_Latin1FromUTF8Bytes.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.CNV_CheckUTF8Bytes.argtypes = [c_char_p, c_int]
_dipki.CNV_CheckUTF8File.argtypes = [c_char_p]
_dipki.CNV_ByteEncoding.argtypes = [c_char_p, c_int, c_char_p, c_int, c_int]
_dipki.CNV_ReverseBytes.argtypes = [c_char_p, c_char_p, c_int]
_dipki.CNV_NumToBytes.argtypes = [c_char_p, c_int, c_int, c_int]
_dipki.CNV_NumFromBytes.argtypes = [c_char_p, c_int, c_int]
_dipki.PEM_FileFromBinFile.argtypes = [c_char_p, c_char_p, c_char_p, c_int]
_dipki.PEM_FileFromBinFileEx.argtypes = [c_char_p, c_char_p, c_char_p, c_int, c_int]
_dipki.PEM_FileToBinFile.argtypes = [c_char_p, c_char_p]
_dipki.RNG_Bytes.argtypes = [c_char_p, c_int, c_void_p, c_int]
_dipki.RNG_Number.argtypes = [c_int, c_int]
_dipki.RNG_BytesWithPrompt.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.RNG_Initialize.argtypes = [c_char_p, c_int]
_dipki.RNG_MakeSeedFile.argtypes = [c_char_p, c_char_p, c_int]
_dipki.RNG_UpdateSeedFile.argtypes = [c_char_p, c_int]
_dipki.RNG_Test.argtypes = [c_char_p, c_int]
_dipki.PAD_BytesBlock.argtypes = [c_char_p, c_int, c_char_p, c_int, c_int, c_int]
_dipki.PAD_UnpadBytes.argtypes = [c_char_p, c_int, c_char_p, c_int, c_int, c_int]
_dipki.PAD_HexBlock.argtypes = [c_char_p, c_int, c_char_p, c_int, c_int]
_dipki.PAD_UnpadHex.argtypes = [c_char_p, c_int, c_char_p, c_int, c_int]
_dipki.WIPE_File.argtypes = [c_char_p, c_int]
_dipki.WIPE_Data.argtypes = [c_void_p, c_int]
_dipki.PWD_Prompt.argtypes = [c_char_p, c_int, c_char_p]
_dipki.PWD_PromptEx.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.PBE_Kdf2.argtypes = [c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_int, c_int]
_dipki.PBE_Kdf2Hex.argtypes = [c_char_p, c_int, c_int, c_char_p, c_char_p, c_int, c_int]
_dipki.ASN1_TextDump.argtypes = [c_char_p, c_char_p, c_int]
_dipki.ASN1_Type.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.SIG_SignData.argtypes = [c_char_p, c_int, c_char_p, c_int, c_char_p, c_char_p, c_char_p, c_int]
_dipki.SIG_SignFile.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.SIG_VerifyData.argtypes = [c_char_p, c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.SIG_VerifyFile.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.SMIME_Wrap.argtypes = [c_char_p, c_char_p, c_char_p, c_int]
_dipki.SMIME_Extract.argtypes = [c_char_p, c_char_p, c_int]
_dipki.SMIME_Query.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
