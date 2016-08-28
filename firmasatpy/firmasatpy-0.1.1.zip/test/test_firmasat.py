#! python2
# -*- coding: utf8 -*-

"""Some tests for `firmasat.py` the Python interface to CryptoSys FirmaSAT."""

# test_firmasat.py: version 0.1.1

# ************************** LICENSE *****************************************
# Copyright (C) 2016 David Ireland, DI Management Services Pty Limited.
# <www.di-mgt.com.au> <www.cryptosys.net>
# This code is provided 'as-is' without any express or implied warranty.
# Free license is hereby granted to use this code as part of an application
# provided this license notice is left intact. You are *not* licensed to
# share any of this code in any form of mass distribution, including, but not
# limited to, reposting on other web sites or in any source code repository.
# ****************************************************************************

from firmasat import *  # @UnusedWildImport
import os
import sys
import pytest
import shutil
import random
from glob import iglob

_MIN_FSA_VERSION = 70310

# Show some info about the core CryptoSys DLL
print "FSA version =", Gen.version()
print "module_name =", Gen.module_name()
print "compile_time =", Gen.compile_time()
print "platform =", Gen.core_platform()
print "licence_type =", Gen.licence_type()
# Show some system values
print "sys.getdefaultencoding()=", sys.getdefaultencoding()
print "sys.getfilesystemencoding()=", sys.getfilesystemencoding()
print "sys.platform()=", sys.platform
print "cwd =", os.getcwd()

if Gen.version() < _MIN_FSA_VERSION:
    raise Exception('Require PKI version ' +
                    str(_MIN_FSA_VERSION) + ' or greater')

# GLOBAL VARS
# Remember CWD where we started
start_dir = os.getcwd()
# Temp directory to use as CWD for tests - set by  `setup_temp_dir()`
ourtmp_dir = ""
# Flag to delete tmp directory when finished - used in `reset_start_dir()`
# Change with command-line argument `nodelete` - see `main()`
delete_tmp_dir = True


# JIGGERY-POKERY FOR A TEMP WORKING DIRECTORY
#    start_dir/
#        test_firmaSello.py  # this module
#        work/             # this _must_ exist
#            <all required test files>
#            tmp.XXXXXXXX/    # created by `setup_temp_dir()`
#                <copy of all required test files>
#                <files created by tests>


def setup_temp_dir():
    """Set up a fresh temp directory to work in."""
    global ourtmp_dir
    # `work` should be a sub-directory of the cwd and must exist
    work_dir = os.path.join(start_dir, "work")
    print "\nExpecting to find work dir:", work_dir
    assert os.path.isdir(work_dir)
    # It should contain all the required test files
    # Create a temp sub-directory in `work` -- random 8 hex digits
    r1 = random.randrange(0, (1 << 16))
    r2 = random.randrange(0, (1 << 16))
    ourtmp_dir = os.path.join(
        work_dir, "tmp." + format(r1, '04X') + format(r2, '04X'))
    os.mkdir(ourtmp_dir)
    assert(os.path.isdir(ourtmp_dir))
    # Copy the required temp files
    for f in iglob(os.path.join(work_dir, "*.*")):
        if (os.path.isfile(f) and not f.endswith('.zip')):
            shutil.copy(f, ourtmp_dir)

    # Set CWD to be inside temp
    os.chdir(ourtmp_dir)
    print "Working in new temp directory:", os.getcwd()


def reset_start_dir():
    """Set CWD back to where we started and delete temp dir."""
    if not os.path.isdir(start_dir):
        return
    if (ourtmp_dir == start_dir):
        return
    os.chdir(start_dir)
    print ""
    # print "CWD:", os.getcwd()
    # Remove the temp direcory
    if (delete_tmp_dir and 'tmp.' in ourtmp_dir):
        print "Removing temp directory:", ourtmp_dir
        shutil.rmtree(ourtmp_dir, ignore_errors=True)
    else:
        print "Temp directory '%s' is left in place." % (ourtmp_dir)


# MORE JIGGERY_POKERY FOR py.test
# Thanks to Brian Okken for the base code
# <http://pythontesting.net/framework/pytest/pytest-session-scoped-fixtures/>

@pytest.fixture(scope="module", autouse=True)
def divider_module(request):
    print("\n   --- module %s() start ---" % request.module.__name__)
    setup_temp_dir()

    def fin():
        print("\n   --- module %s() done ---" % request.module.__name__)
        reset_start_dir()
    request.addfinalizer(fin)


@pytest.fixture(scope="function", autouse=True)
def divider_function(request):
    print("\n   --- function %s() start ---" % request.function.__name__)
    os.chdir(ourtmp_dir)

    def fin():
        print("\n   --- function %s() done ---" % request.function.__name__)
        os.chdir(start_dir)
    request.addfinalizer(fin)


# FILE-RELATED UTILITIES
def read_binary_file(fname):
    with open(fname, "rb") as f:
        return bytearray(f.read())


def read_text_file(fname):
    with open(fname, "rb") as f:
        return str(f.read())


def write_file(fname, data):
    with open(fname, "wb") as f:
        f.write(data)


def _print_file(fname):
    """Print contents of text file"""
    s = read_text_file(fname)
    print s


def _dump_file(fname):
    """Print contents of text file with filename header and rulers"""
    s = read_text_file(fname)
    ndash = (24 if len(s) > 24 else len(s))  # hack
    print "FILE:", fname
    print "-" * ndash
    print s
    print "-" * ndash


def _file_has_bom(fname):
    """Returns True if file has a UTF-8 BOM or False if not."""
    buf = read_binary_file(fname)
    if (len(buf) < 3):
        return False
    # BOM consists of three bytes (0xEF, 0xBB, 0xBF)
    return (buf[0] == 0xEF and buf[1] == 0xBB and buf[2] == 0xBF)


# ERROR
def disp_error(n):
    """Display details of last error."""
    s = Err.last_error()
    print "ERROR %d: %s: %s" % (n, Err.error_lookup(n), "\n" + s if s else "")


###################
# THE TESTS PROPER
###################

def test_version():
    print "VERSION:", Gen.version()
    assert Gen.version() >= _MIN_FSA_VERSION


def test_error_lookup():
    print "\nLOOKUP SOME ERROR CODES..."
    for n in range(10):
        s = Err.error_lookup(n)
        print "error_lookup(" + str(n) + ")=" + s
        assert(len(s) > 0)


def test_make_digest():
    print "\nFORM MESSAGE DIGESTS..."
    fname = 'ejemplo_v32-base2015.xml'
    print "FILE:", fname
    dig = Sello.make_digest(fname)
    print "DEFAULT:", dig
    dig = Sello.make_digest(fname, HashAlg.SHA1)
    print "SHA-1  :", dig

    dig = Sello.make_digest('ejemplo_v32.xml')
    print "dig    :", dig


def test_make_pipestring_and_sig():
    print "\nCREATE PIPE STRING..."
    fname = 'ejemplo_v32-base2015.xml'
    print "FILE:", fname
    s = Sello.make_pipestring(fname)
    print s
    keyfile = 'emisor.key'
    passwd = '12345678a'
    sig = Sello.make_sig(fname, keyfile, passwd)
    print "SIG:", sig


def test_query_cert():
    print "\nQUERY X.509 CERT..."
    fname = 'ejemplo_v32-signed2015.xml'
    print "FILE:", fname
    query = 'serialNumber'
    s = Pkix.query_cert(fname, query)
    print "Pkix.query_cert(" + query + ")=[" + s + "]"
    query = 'keySize'
    s = Pkix.query_cert(fname, query)
    print "Pkix.query_cert(" + query + ")=[" + s + "]"
    query = 'organizationName'
    s = Pkix.query_cert(fname, query)
    print "Pkix.query_cert(" + query + ")=[" + s + "]"

    fname = "AC4_SAT.cer"
    print "FILE:", fname
    query = 'serialNumber'
    s = Pkix.query_cert(fname, query)
    print "Pkix.query_cert(" + query + ")=[" + s + "]"
    query = 'keySize'
    s = Pkix.query_cert(fname, query)
    print "Pkix.query_cert(" + query + ")=[" + s + "]"

    try:
        _ = Pkix.query_cert(fname, "BADQUERY")
    except Error as e:
        print "(Expected) Error:", e
    else:
        raise Exception("Test should have failed.")

    n = Pkix.query_cert('AC4_SAT.cer', 'keySize')
    print "n =", n
    n = Pkix.query_cert('AC4_SAT.cer', Pkix.Query.KEYSIZE)
    print "n =", n
    s = Pkix.query_cert('ejemplo_v32.xml', 'serialNumber')
    print "s =", s


def test_validate_xml():
    print "\nVALIDATE XML SYNTAX..."

    # A valid XML file
    n = Xmlu.validate_xml('ejemplo_v32.xml')
    assert(0 == n)

    fname = 'ejemplo_v32.xml'
    n = Xmlu.validate_xml(fname)
    print "validate_xml('%s') returns %d (expected zero => OK)" % (fname, n)

    print "EXPECTING ERRORS..."
    # XML with a non-conforming attribute
    fname = "V3_2_BadCurp.xml"
    n = Xmlu.validate_xml(fname)
    print "validate_xml('%s') returns %d (expected nonzero error)" % (fname, n)
    if (n != 0):
        disp_error(n)
    assert(n != 0)
    # print "But..."
    n = Xmlu.validate_xml(fname, loose=True)
    print "validate_xml('%s', loose) returns %d (expected zero => OK)" % (fname, n)
    assert(0 == n)

    # Not an XML file
    fname = "emisor.cer"
    n = Xmlu.validate_xml(fname)
    print "validate_xml('%s') returns %d (expected nonzero error)" % (fname, n)
    if (n != 0):
        disp_error(n)
    assert(n != 0)

    print "...END OF EXPECTED ERRORS."


def test_get_attribute():
    print "\nGET ATTRIBUTE FROM XML..."

    fname = 'ejemplo_v32.xml'
    s = Xmlu.get_attribute(fname, "pais", "cfdi:ExpedidoEn")
    print "Xmlu.get_attribute() returns %s" % (s)

    # Get N'th elements
    print Xmlu.get_attribute(fname, "descripcion", "Concepto[1]")
    print Xmlu.get_attribute(fname, "descripcion", "Concepto[2]")
    print Xmlu.get_attribute(fname, "descripcion", "Concepto[3]")


def test_receipt_id():
    print "\nGET COMPROBANTE VERSION OR ID NUMBER..."

    n = Xmlu.receipt_version('ejemplo_v32.xml')
    assert(32 == n)

    # Other types of files
    for (fname, exp) in [
        ("ejemplo_v32.xml", 32),
        ("Ejemplo_Retenciones-base.xml", 1010),
        ("AAA010101AAA201501CT-base.xml", 2011),
        ("AAA010101AAA201501BN-base.xml", 2111),
        ("ConVolE12345-signed2015.xml", 4011),
    ]:
        print "FILE:", fname
        n = Xmlu.receipt_version(fname)
        print "  receipt_version() returns %d (expected %d)" % (n, exp)
        assert(n == exp)
        # Show root element of document
        print "  ROOT=%s" % (Xmlu.get_attribute(fname, "", ""))


def test_uuid():
    print "\nTEST RANDOM UUID..."
    for dummy in range(5):
        s = Pkix.uuid()
        print s


def test_key_string():
    print "\nTEST KEY AS STRING..."

    s = Pkix.get_key_as_string('emisor.key', '12345678a')
    assert(len(s) > 0)
    s = Pkix.get_key_as_string(
        'emisor.key', '12345678a', Pkix.KeyOpt.ENCRYPTED_PEM)
    assert(len(s) > 0)

    fname = "emisor.key"
    pwd = '12345678a'   # CAUTION: do not hardcode passwords
    s = Pkix.get_key_as_string(fname, pwd)
    print "Pkix.get_key_as_string('%s'):\n%s" % (fname, s)
    s = Pkix.get_key_as_string(fname, pwd, Pkix.KeyOpt.ENCRYPTED_PEM)
    print "Pkix.get_key_as_string('%s', ENCRYPTED_PEM):\n%s" % (fname, s)


def test_cert_string():
    print "\nTEST CERT AS STRING..."

    s = Pkix.get_cert_as_string('emisor.cer')
    assert(len(s) > 0)
    s = Pkix.get_cert_as_string('ejemplo_v32.xml')
    assert(len(s) > 0)

    fname = "emisor.cer"
    s = Pkix.get_cert_as_string(fname)
    print "Pkix.get_cert_as_string('%s'):\n%s" % (fname, s)
    fname = 'ejemplo_v32.xml'
    s = Pkix.get_cert_as_string(fname)
    print "Pkix.get_cert_as_string('%s'):\n%s" % (fname, s)

    # We can query this string directly as though it were an X.509 file
    print "Query the string directly..."
    rfc = Pkix.query_cert(s, Pkix.Query.RFC)
    print "RFC =", rfc
    assert(len(rfc) > 0)
    alg = Pkix.query_cert(s, Pkix.Query.SIGALG)
    print "alg =", alg
    assert(len(alg) > 0)


def test_write_pfx():
    print "\nWRITE PFX FILE..."

    keyFile = "emisor.key"
    certFile = "emisor.cer"
    pfxFile = "emisor.pfx"
    n = Pkix.write_pfx_file(pfxFile, "password1",
                            keyFile, '12345678a', certFile)
    assert(0 == n)
    print "Created new file '%s'" % (pfxFile)
    contents = read_text_file(pfxFile)
    print "Contents:\n", contents


def test_check_key_cert():
    print "\nCHECK KEY MATCHES CERT..."

    # Key and cert match
    keyFile = "emisor.key"
    certFile = "emisor.cer"
    n = Pkix.check_key_and_cert(keyFile, '12345678a', certFile)
    print "Pkix.check_key_and_cert() returns %d (expecting 0 => OK)" % (n)

    print "EXPECTING ERRORS..."

    # Key and cert DO NOT match
    keyFile = "emisor.key"
    certFile = "pac.cer"
    n = Pkix.check_key_and_cert(keyFile, '12345678a', certFile)
    print "Pkix.check_key_and_cert() returns %d" % (n)
    disp_error(n)

    # password is wrong
    keyFile = "emisor.key"
    certFile = "pac.cer"
    n = Pkix.check_key_and_cert(keyFile, 'wrong password', certFile)
    print "Pkix.check_key_and_cert() returns %d" % (n)
    disp_error(n)

    # Key file is invalid
    keyFile = "ejemplo_v32.xml"
    certFile = "pac.cer"
    n = Pkix.check_key_and_cert(keyFile, '12345678a', certFile)
    print "Pkix.check_key_and_cert() returns %d" % (n)
    disp_error(n)

    print "...END OF EXPECTED ERRORS."


def test_sign_xml():
    print "\nSIGN XML FILE..."

    basefile = "ejemplo_v32-base2015.xml"
    newfile = "ejemplo_v32-new-signed.xml"
    n = Sello.sign_xml(newfile, basefile, "emisor.key",
                       '12345678a', "emisor.cer")
    print "Sello.sign_xml() returns %d (expecting 0 => OK)" % (n)
    print "Created new XML file '%s'" % (newfile)


def test_extract_digest():
    print "\nEXTRACT DIGEST FROM SELLO..."

    fname = "ejemplo_v32-signed2015.xml"
    extr_dig = Sello.extract_digest_from_sig(fname)
    print extr_dig

    made_dig = Sello.make_digest(fname)
    print made_dig


def test_verify_sig():
    print "\nVERIFY SIGNATURE IN XML FILE..."

    n = Sello.verify_sig('ejemplo_v32-signed2015.xml')
    print "Sello.verify_sig() returns %s" % (n)

    # Override certificado included in XML with (correct) cert file
    n = Sello.verify_sig('ejemplo_v32-signed2015.xml', 'emisor.cer')
    print "Sello.verify_sig() returns %s" % (n)

    print "ERRORS EXPECTED..."

    # Override with wrong certificate file
    n = Sello.verify_sig('ejemplo_v32-signed2015.xml', 'pac.cer')
    print "Sello.verify_sig() returns %s" % (n)
    disp_error(n)

    # Sello has been changed
    n = Sello.verify_sig('ejemplo_v32-badsign.xml')
    print "Sello.verify_sig() returns %s" % (n)
    disp_error(n)

    # File does not exist
    n = Sello.verify_sig('missing.xml')
    print "Sello.verify_sig() returns %s" % (n)
    disp_error(n)

    # Not an XML file
    n = Sello.verify_sig('pac.cer')
    print "Sello.verify_sig() returns %s" % (n)
    disp_error(n)

    print "...END OF EXPECTED ERRORS."


def test_fix_bom():
    print "\nFIX BOM IN XML FILE..."

    infile = "ejemplo_v32-base2015.xml"
    outfile = "ejemplo_v32-nobom.xml"
    print "Create a signed XML file with no BOM..."
    n = Sello.sign_xml(outfile, infile, "emisor.key", '12345678a',
                       "emisor.cer", signopts=Sello.SignOpts.NOBOM)
    print "Sello.sign_xml() returns %d (expecting 0 => OK)" % (n)
    print "Created new XML file '%s'" % (outfile)
    has_bom = _file_has_bom(outfile)
    print "File %s a UTF-8 BOM" % ("DOES NOT have" if not has_bom else "HAS")

    print "Now add a BOM to it..."
    infile = outfile
    outfile = "ejemplo_v32-withbom.xml"
    n = Xmlu.fix_bom(outfile, infile)
    print "Xmlu.fix_bom() returns %d (expecting 0 => OK)" % (n)
    print "Created new XML file '%s'" % (outfile)
    has_bom = _file_has_bom(outfile)
    print "File %s a UTF-8 BOM" % ("DOES NOT have" if not has_bom else "HAS")


def test_sign_xml_to_buf():
    print "\nSIGN XML FILE TO BUFFER..."

    basefile = "ejemplo_v32-base2015.xml"
    print "bytes <-- file"
    xmlsigned = Sello.sign_xml_file_to_buf(
        basefile, "emisor.key", '12345678a', "emisor.cer")
    print xmlsigned
    # Write to disk so we can examine later
    write_file("frombuf1.xml", xmlsigned)

    # Read in file to a byte array, then sign to a buffer
    xmlbase = read_binary_file(basefile)
    print "Read in %d bytes from file" % (len(xmlbase))
    print "bytes <-- bytes"
    xmlsigned = Sello.sign_xml_data_to_buf(
        xmlbase, "emisor.key", '12345678a', "emisor.cer", signopts=Sello.SignOpts.USEEMPTYELEMENTS)
    print xmlsigned[0:60] + '\n ...[snip]... \n' + xmlsigned[-60:]
    write_file("frombuf2.xml", xmlsigned)

    # We can pass key file and certificate as "PEM" strings.
    # The "BEGIN/END" encapsulation is optional for a certificate,
    # but is required for the encrypted private key.
    # These strings are from `emisor-pem.cer` and `emisor-pem.key`,
    # respectively
    certdata = (
        "-----BEGIN CERTIFICATE-----"
        "MIIEdDCCA1ygAwIBAgIUMjAwMDEwMDAwMDAxMDAwMDU4NjcwDQYJKoZIhvcNAQEF"
        "BQAwggFvMRgwFgYDVQQDDA9BLkMuIGRlIHBydWViYXMxLzAtBgNVBAoMJlNlcnZp"
        "Y2lvIGRlIEFkbWluaXN0cmFjacOzbiBUcmlidXRhcmlhMTgwNgYDVQQLDC9BZG1p"
        "bmlzdHJhY2nDs24gZGUgU2VndXJpZGFkIGRlIGxhIEluZm9ybWFjacOzbjEpMCcG"
        "CSqGSIb3DQEJARYaYXNpc25ldEBwcnVlYmFzLnNhdC5nb2IubXgxJjAkBgNVBAkM"
        "HUF2LiBIaWRhbGdvIDc3LCBDb2wuIEd1ZXJyZXJvMQ4wDAYDVQQRDAUwNjMwMDEL"
        "MAkGA1UEBhMCTVgxGTAXBgNVBAgMEERpc3RyaXRvIEZlZGVyYWwxEjAQBgNVBAcM"
        "CUNveW9hY8OhbjEVMBMGA1UELRMMU0FUOTcwNzAxTk4zMTIwMAYJKoZIhvcNAQkC"
        "DCNSZXNwb25zYWJsZTogSMOpY3RvciBPcm5lbGFzIEFyY2lnYTAeFw0xMjA3Mjcx"
        "NzAyMDBaFw0xNjA3MjcxNzAyMDBaMIHbMSkwJwYDVQQDEyBBQ0NFTSBTRVJWSUNJ"
        "T1MgRU1QUkVTQVJJQUxFUyBTQzEpMCcGA1UEKRMgQUNDRU0gU0VSVklDSU9TIEVN"
        "UFJFU0FSSUFMRVMgU0MxKTAnBgNVBAoTIEFDQ0VNIFNFUlZJQ0lPUyBFTVBSRVNB"
        "UklBTEVTIFNDMSUwIwYDVQQtExxBQUEwMTAxMDFBQUEgLyBIRUdUNzYxMDAzNFMy"
        "MR4wHAYDVQQFExUgLyBIRUdUNzYxMDAzTURGUk5OMDkxETAPBgNVBAsTCFVuaWRh"
        "ZCAxMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC2TTQSPONBOVxpXv9wLYo8"
        "jezBrb34i/tLx8jGdtyy27BcesOav2c1NS/Gdv10u9SkWtwdy34uRAVe7H0a3VMR"
        "LHAkvp2qMCHaZc4T8k47Jtb9wrOEh/XFS8LgT4y5OQYo6civfXXdlvxWU/gdM/e6"
        "I2lg6FGorP8H4GPAJ/qCNwIDAQABox0wGzAMBgNVHRMBAf8EAjAAMAsGA1UdDwQE"
        "AwIGwDANBgkqhkiG9w0BAQUFAAOCAQEATxMecTpMbdhSHo6KVUg4QVF4Op2IBhiM"
        "aOrtrXBdJgzGotUFcJgdBCMjtTZXSlq1S4DG1jr8p4NzQlzxsdTxaB8nSKJ4KEMg"
        "IT7E62xRUj15jI49qFz7f2uMttZLNThipunsN/NF1XtvESMTDwQFvas/Ugig6qwE"
        "fSZc0MDxMpKLEkEePmQwtZD+zXFSMVa6hmOu4M+FzGiRXbj4YJXn9Myjd8xbL/c+"
        "9UIcrYoZskxDvMxc6/6M3rNNDY3OFhBK+V/sPMzWWGt8S1yjmtPfXgFs1t65AZ2h"
        "cTwTAuHrKwDatJ1ZPfa482ZBROAAX1waz7WwXp0gso7sDCm2/yUVww=="
        "-----END CERTIFICATE-----"
    )
    keydata = (
        "-----BEGIN ENCRYPTED PRIVATE KEY-----"
        "MIICxjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQI3V0iJrMlAI0CAggA"
        "MBQGCCqGSIb3DQMHBAgmAnxnceS9FgSCAoBeM47Z7bIErpBCcTTUqChTzglQ2Om+"
        "Nw4Nv0YZZkw8T0iLknP5J+p0EJHDQzATqHC1VZmG8+S23yJWSpYKzikQ0EdQCg3y"
        "pl6QP55wdZ6DmkJQPo4cE+Z9elLT4QDRH//bJbZlnUtwKlu0ldMFNlBdAz/vYM4C"
        "mad/cYIaR2tEJrJQvOiT4Z+c5Thf/3kLr5ohtVi7IDCFrIuSk0y0994rW4yGXQT7"
        "/licNrOSDnBIWYP1poYa5YBFw6KMqA+uC7xwu6XGpdMJ3pyaogZUlw0MwL0mnWNI"
        "DUkKm0lBrM0bEXZJgVbMzBokUupOMq6RAIOb6NXRREAw6mpyiekMNUE2ajXB2Xlj"
        "1O12LqBEPMfdjeeQ1oakUuAfrTKiFIREcSW8472Xcmzu40u+zTCJVefpgNb6FF6V"
        "L3QH3LZ+F2+A92rXn1gZETlHn9MjMfZyh7NUUbZ+BCpq0U2lyARbTZ2T+LvHP1gk"
        "2oEDB/X+otXuK0cMxj8yG4tc5g7w7xo8GCMAu8zmKQa4pNd5+vND4JgwIaSWC5yW"
        "EB0/E5qszMij2l1Ibni3Uj9HB8baf0ZU9hMahP4hjF1hFb4HfRxcmYOGyfldMCnr"
        "1zQ0IZXCS5ki/xdrvxgkj6CEl9dXutPBrbg/mIPJLIkJPGQ2T78tlwvFl5C5i9U9"
        "sOha2UmVXtDwg0zwWqLgS/6oQNYouQQlFbeH3jEYgHGENqunsIb0Nt4HBSQq6NgH"
        "XGK7WRaLeDPIDr7j85cBdycuKXPH4Vtb8qx9dH4veKKz6ymbiHtXY63+3J4Geh6t"
        "IzLduuX0CBiLob0R+gorwUK28i6bS373/d/GQoWOdBmSSws2BaHEGBmU"
        "-----END ENCRYPTED PRIVATE KEY-----"
    )
    # Note that all parameters are passed as strings here: no files involved
    xmlsigned = Sello.sign_xml_data_to_buf(
        xmlbase, keydata, '12345678a', certdata)
    print xmlsigned[0:60] + '\n ...[snip]... \n' + xmlsigned[-60:]
    print "type(xmlsigned)=", type(xmlsigned)
    write_file("frombuf3.xml", xmlsigned)


def test_tfd():
    print "\nOPERATIONS ON THE TIMBRE FISCAL DIGITAL (TFD)..."
    print "\nCREATE CADENA ORIGINAL DEL TIMBRE FISCAL DIGITAL (PIPESTRING FOR TFD):"
    fname = "ejemplo_v32-tfd2015.xml"
    s = Tfd.make_pipestring(fname)
    print s
    # Form the digest from the element nodes in the XML doc
    s = Tfd.make_digest(fname)
    print s
    # Extract the digest from the signature value using the PAC's cert
    certfile = "pac.cer"
    s1 = Tfd.extract_digest_from_sig(fname, certfile)
    print s1
    # Should be the same, but ignore case when comparing
    assert(s1.lower() == s.lower())

    print "\nPRETEND WE ARE A PAC WITH A KEY ALLOWED TO SIGN THE TFD:"
    # Create a TFD signature string we could paste into the `selloSAT` node
    fname = "ejemplo_v32-tfd2015.xml"
    certfile = "pac.cer"
    keyfile = "pac.key"
    password = "12345678a"
    s = Tfd.make_sig(fname, keyfile, password)
    print s
    # Compare with actual `selloSAT` in doc
    s1 = Xmlu.get_attribute(fname, "selloSAT", "TimbreFiscalDigital")
    print s1
    assert s == s1

    print "\nVERIFY SIGNATURE IN TFD SELLOSAT:"
    n = Tfd.verify_sig(fname, certfile)
    print "Tfd.verifySignature() returns %d (expected 0)" % (n)
    assert 0 == n

    print "\nADD A TFD ELEMENT TO A SIGNED CFDI DOCUMENT USING PAC KEY:"
    # Base file is signed but has no TFD element
    fname = "ejemplo_v32-signed2015.xml"
    newname = "ejemplo_v32-new-tfd.xml"
    # We have the PAC's private key and cert to do the signing
    certfile = "pac.cer"
    keyfile = "pac.key"
    password = "12345678a"
    n = Tfd.add_signed_tfd(newname, fname, keyfile, password, certfile)
    print "Tfd.add_signed_tfd('%s'-->'%s') returns %d" % (fname, newname, n)
    assert 0 == n
    # Did we make a valid XML file?
    n = Xmlu.validate_xml(newname)
    print "Xmlu.validate_xml() returned %d" % (n)
    assert 0 == n
    # Does it have a valid selloSAT in the TFD?
    n = Tfd.verify_sig(newname, certfile)
    print "Tfd.verify_sig() returned %d" % (n)
    assert 0 == n
    # Show the pipe string. NB different each time
    #  -- timestamped using the system clock and a fresh UUID is generated
    s = Tfd.make_pipestring(newname)
    print s


def main():
    do_all = True
    for arg in sys.argv:
        global delete_tmp_dir
        if (arg == 'nodelete'):
            delete_tmp_dir = False
        elif (arg == 'some'):
            do_all = False
    setup_temp_dir()

    # DO THE TESTS - EITHER SOME OR ALL
    if (do_all):
        print "DOING ALL TESTS...\n"
        test_version()
        test_error_lookup()
        test_make_digest()
        test_make_pipestring_and_sig()
        test_query_cert()
        test_uuid()
        test_validate_xml()
        test_receipt_id()
        test_cert_string()
        test_key_string()
        test_write_pfx()
        test_check_key_cert()
        test_sign_xml()
        test_fix_bom()
        test_sign_xml_to_buf()
        test_get_attribute()
        test_verify_sig()
        test_extract_digest()
        test_tfd()

    else:   # just do some tests: comment out as necessary
        print "ONLY DOING SOME TESTS...\n"
        test_version()
#         test_error_lookup()
#         test_make_digest()
#         test_make_pipestring_and_sig()
#         test_query_cert()
#         test_uuid()
#         test_validate_xml()
        test_receipt_id()
#         test_cert_string()
#         test_key_string()
#         test_write_pfx()
#         test_check_key_cert()
#         test_sign_xml()
#         test_fix_bom()
#         test_sign_xml_to_buf()
#         test_get_attribute()
#         test_verify_sig()
#         test_extract_digest()
#         test_tfd()

    reset_start_dir()
    print "ALL DONE."


if __name__ == "__main__":
    main()
