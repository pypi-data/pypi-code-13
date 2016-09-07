#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
   send_ses_email.py
   =================

   Send email messages using the AWS SES. Credentials are loaded from a
   configuration file.

   (c) 2014, Edward J. Stronge Available under the MIT License - see LICENSE
   for details.
"""
import argparse
from email.mime.text import MIMEText
import smtplib
import sys
import time

from send_ses_message.send_smtp_ses_email import (get_smtp_parameters, 
    get_server_reference)


def main():
    """
       Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Simple email tool backed by the Amazon SES SMTP interface")
    parser.add_argument('-s', '--subject', help="Subject of email")
    parser.add_argument('-f', '--from_email', help="Email sender")
    parser.add_argument(
        '--config_file', default='smtp_credentials.cfg',
        help="CFG file of SMTP user credentials. Must define variables"
             "USERNAME, SMTP_PASSWORD, AWS_SMTP_ENDPOINT, and AWS_SMTP_PORT"
             "in a 'default' section.")
    parser.add_argument('to_email', help="Email recipient")
    parser.add_argument(
        'message', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
        help="File containing email text. By default, reads text from stdin")

    args = parser.parse_args()
    configuration_params = get_smtp_parameters([args.config_file])

    message = MIMEText(args.message.read())
    message['Subject'] = args.subject
    message['From'] = args.from_email
    message['To'] = args.to_email
    try:
        server = get_server_reference(**configuration_params)
        server.sendmail(args.from_email, args.to_email, message.as_string())
    except smtplib.SMTPException:
        server.quit()
        time.sleep(30)
        server = get_server_reference(**configuration_params)
        server.sendmail(args.from_email, args.to_email, message.as_string())


if __name__ == '__main__':
    main()
