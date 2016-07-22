# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-01 13:17:56
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-05 23:42:42

import re
from unit import *

class Normalizer():

    re_digits = re.compile(r'\d+')
    re_price_unit = re.compile(r'(?:'+ r'|'.join(UNIT_PRICE_UNITS) + r'){1,2}')
    reg_time_units = r'(?:'+ \
                r'(?:\d{1,3}[ ]?(?:' + r'|'.join(UNIT_TIME_HOUR+UNIT_TIME_MINUTE) + r'))' + r'|' \
                r'(?:' + r'|'.join(UNIT_TIME_UNITS) + r')' \
                r')'
    re_time_unit = re.compile(reg_time_units)



    def __init__(self):
        pass

    def normalize(self, text):
        price = ''
        price_unit = ''
        time_unit = ''

        if len(Normalizer.re_digits.findall(text)) == 2:
            tunit = Normalizer.re_time_unit.search(text)
            if tunit:
                time_unit = tunit.group(0)

                text = Normalizer.re_time_unit.sub('', text)

            p = Normalizer.re_digits.search(text)
            if p:
                price = p.group(0)

        else:
            p = Normalizer.re_digits.search(text)
            if p:
                price = p.group(0)
                text = Normalizer.re_digits.sub('', text)

            tunit = Normalizer.re_time_unit.search(text)
            if tunit:
                time_unit = tunit.group(0)
                
        punit = Normalizer.re_price_unit.search(text)
        if punit:
            price_unit = punit.group(0)

        ht = {}
        ht['price'] = price
        ht['price_unit'] = price_unit
        ht['time_unit'] = time_unit
        return ht


    def normalize_from_list(self, text_list):
        return [self.normalize(text) for text in text_list]



if __name__ == '__main__':
    # text = 'half hour 100'
    # text = '45 min 400 rose'
    # text = '80 hh'
    text = '1 hr $350'
    normalizer = Normalizer()
    print normalizer.normalize(text)




