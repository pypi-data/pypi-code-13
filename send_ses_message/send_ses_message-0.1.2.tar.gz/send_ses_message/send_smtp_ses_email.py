# -*- coding: utf-8 -*-
"""
send_ses_email.py
=================

Send email messages using the AWS SES. Credentials are loaded from a
configuration file.

(c) 2014, Edward J. Stronge Available under the MIT License - see LICENSE
for details.
"""

import sys

PYTHON2 = sys.version_info.major == 2

if PYTHON2:
    import ConfigParser
    configparser = ConfigParser
else:
    import configparser

import smtplib


def get_server_reference(
        username, smtp_password, aws_smtp_endpoint, aws_smtp_port, **kwargs):
    """
    Returns smtplib.smtp reference using the specified parameters.
    Call sendmail on the returned reference to send emails.

    See the example configuration file for explanations on where to
    find these parameters.

    kwargs is present to allow users to use dict unpacking from
    configuration files even when those contain extra parameters
    that we don't need here.
    """
    smtp_con = smtplib.SMTP(
        host=aws_smtp_endpoint, port=aws_smtp_port, timeout=10)
    smtp_con.starttls()
    smtp_con.ehlo()
    smtp_con.login(username, smtp_password)
    # Will need to re-obtain this reference occasionally as server
    # connections aren't maintained long-term
    return smtp_con


def get_smtp_parameters(config_file_sequence):
    """
    Read the configuration files in config_file_sequence
    and return a dictionary of the parameter specified
    in their 'default' section.
    """
    config_parser = configparser.SafeConfigParser()
    config_parser.read(config_file_sequence)
    return {i[0].lower(): i[1] for i in config_parser.items('default')}
