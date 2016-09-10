"""
    Targetpay Python module
    Copyright (C) 2016, Balkan Technologies EOOD & Co. KD

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    For more information: info@balkan.tech
"""

import requests
from lxml import etree

DEBUG_MODE = True

METHODS = (
    ('IDL', 'iDeal'),
    ('MRC', 'Mister Cash'),
    ('SOF', 'Sofort banking')
)

VERIFICATION = {
    'IDL': 'ideal',
    'MRC': 'mrcash',
    'SOF': 'directebanking',
}

SOFORT_TYPES = {
    'PHYSICAL': 1,
    'DIGITAL': 2,
    'DIGITAL_ADULT': 3
}

SOFORT_COUNTRIES = {
    'DE': 49,
    'AT': 43,
    'CH': 41,
    'BE': 32,
    'IT': 39,
}

def to_cents(amount):
    # Check is amount is float, if so convert to int and cents
    if isinstance(amount, float):
        amount = int(amount * 100)
    else:
        amount = amount * 100  # convert to cents
    return amount

class TargetPay(object):
    def __init__(self, rtlo, test = False):
        self.rtlo = rtlo
        self.test = test
        self.payment_url = None
        self.transaction_id = None
        self.method = None
        self.methodtransaction_id = None
        self.code = None
        self.explanation = None
        self.paid = False
        self.cname = None
        self.cbank = None

    def process_response(self, response, verification = False):
        if DEBUG_MODE:
            print response.content

        try:
            r = response.content.split(' ')
            status = r[0]
        except:
            return False

        if status == '000000':
            self.success = True
            self.explanation = None
            self.code = None

            if not verification:
                print r
                (self.transaction_id, self.payment_url) = r[1].split('|')
            else:
                self.paid = True

            return True
        else:
            self.success = False
            self.paid = False
            self.code = status
            self.explanation = response.content[7:]

            return False

    def verify_payment(self, once=True):
        if self.method:
            method = VERIFICATION[self.method]

            data = {
                'rtlo': self.rtlo,
                'trxid': self.transaction_id
            }

            data['once'] = 1 if once else 0
            if (self.method == 'MRC' or self.method == 'SOF') and self.test:
                data['test'] = 1

            if DEBUG_MODE:
                print data

            self.process_response(requests.post('https://www.targetpay.com/%s/check' % method, data=data),
                                  verification=True)

            return self
        return None

    def callback(self, cname = None, cbank = None, idealtrxid = None):
        if self.method == 'IDL':
            if idealtrxid:
                self.methodtransaction_id = idealtrxid
            else:
                raise Exception('No idealtrxid has been provided')
            if cname:
                self.cname = cname
            if self.cbank:
                self.cbank = cbank

        return self.verify_payment(once = False)

    def ideal_banks(self, as_dict = False):
        url = 'https://www.targetpay.com/ideal/getissuers?ver=3&format=xml'
        req = requests.get(url)
        doc = etree.fromstring(req.content)
        issuers_array = []
        issuers_dict = {}

        for issuer in doc.findall('issuer'):
            if not as_dict:
                issuers_array.append([issuer.get('id'), issuer.text])
            else:
                issuers_dict[issuer.get('id')] = issuer.text
        return issuers_array if not as_dict else issuers_dict

    def ideal_payment(self, description, amount, return_url, cancel_url = None, report_url = None, bank = None, ver = 3):
        self.method = 'IDL'
        amount = to_cents(amount)

        data = {
            'rtlo': self.rtlo,
            'description': description,
            'amount': amount,
            'returnurl': return_url,
            'ver': ver,
        }

        if bank:
            data['bank'] = bank

        if cancel_url:
            data['cancelurl'] = cancel_url

        if report_url:
            data['reporturl'] = report_url

        if self.test:
            data['test'] = 1

        if DEBUG_MODE:
            print data

        self.process_response(requests.post('https://www.targetpay.com/ideal/start', data = data))

        return self

    def mrcash_payment(self, description, amount, ip, return_url, report_url = None, language = 'EN'):
        self.method = 'MRC'
        amount = to_cents(amount)

        data = {
            'rtlo': self.rtlo,
            'description': description,
            'amount': amount,
            'returnurl': return_url,
            'userip': ip,
            'lang': language
        }

        if report_url:
            data['reporturl'] = report_url

        if DEBUG_MODE:
            print data

        self.process_response(requests.post('https://www.targetpay.com/mrcash/start', data = data))

        return self

    def sofort_payment(self, description, amount, ip, country, payment_type, return_url, report_url = None, language = 'EN'):
        self.method = 'SOF'
        amount = to_cents(amount)

        data = {
            'rtlo': self.rtlo,
            'description': description,
            'amount': amount,
            'country': country,
            'type': payment_type,
            'returnurl': return_url,
            'userip': ip,
            'lang': language
        }

        if report_url:
            data['reporturl'] = report_url

        if DEBUG_MODE:
            print data

        self.process_response(requests.post('https://www.targetpay.com/directebanking/start', data = data))

        return self