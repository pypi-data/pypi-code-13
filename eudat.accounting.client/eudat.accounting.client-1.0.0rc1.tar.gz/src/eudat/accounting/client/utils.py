# utilties module from eudat.accounting.client
# collects methods that could be useful for client code as well


USERKEY = "ACCOUNTING_USER"
PWKEY = "ACCOUNTING_PW"
URL_PATTERN = "%s/%s/%s/addRecord?"

import os
import sys
import requests

from eudat.accounting.client import LOG

def getCredentials(args):
    """Extracts and returns (username, password) from args.
    Looks into environment varaibles ACCOUNTING_USER and
    ACCOUNTING_PW respectively if not found in args.
    Terminates if not found"""

    user = args.user
    if not user:
        user = os.getenv(USERKEY)
    pw = args.password
    if not pw:
        pw = os.getenv(PWKEY)

    if not user:
        msg = "No user id provided"
        LOG.error(msg)
        sys.exit(msg)
    if not pw:
        msg = "No password provided"
        LOG.error(msg)
        sys.exit(msg)
    LOG.info("Credentials found")
    return (user, pw)

def getUrl(args):
    """Constructs the URL to call based on the parameters provided"""
    url = URL_PATTERN % (args.base_url, args.domain, args.account)
    LOG.info("URL: " + url)
    return url
    
def getData(args):
    """builds a query string including the data"""
    core_pattern = "core.%s:record=%s"
    meta_pattern = "meta.%s:record=%s"
    vars = []
    vars.append('account=%s' % args.account)
    if args.key:
        vars.append('key=%s' % args.key)
    for k in ['type', 'value', 'unit']:
        vars.append(core_pattern % (k, getattr(args, k)))
    hasNumber = False
    for k in ['service', 'number', 'object_type', 'measure_time', 'comment']:
        value = getattr(args, k)
        if k=='number' and value:
            hasNumber = True
        if value:
            if k=='object_type' and not hasNumber:
                continue
            vars.append(meta_pattern % (k, value))
    qstring = '&'.join(vars)
    LOG.info("query string: " + qstring)
    return qstring

def call(cred, url, data):
    call_url = url+data
    r = requests.post(call_url, auth=cred)
    # TODO: add error handling
    return r
