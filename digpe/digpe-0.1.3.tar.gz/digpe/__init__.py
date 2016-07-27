# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-06-30 11:29:35
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-27 14:14:34

from preprocessor import Preprocessor
from extractor import Extractor
from normalizer import Normalizer
from unit import * 
import re


PE_DICT_NAME_PRICE = 'price'
PE_DICT_NAME_PPH = 'price_per_hour'

PE_JSON_NAME_PRICE = 'price'
PE_JSON_NAME_PRICE_UNIT = 'price_unit'
PE_JSON_NAME_TIME_UNIT = 'time_unit'

class DIGPE():

    def __init__(self):
        self.preprocessor = Preprocessor()
        self.extractor = Extractor()
        self.normalizer = Normalizer()

    re_digits = re.compile(r'\d+')
    re_alphabet = re.compile(r'[a-z ]+')

    def extract(self, text):
        cleaned_text_list = self.preprocessor.preprocess(text)
        extracted_text_list = self.extractor.extract_from_list(cleaned_text_list)
        normalized_text_list = self.normalizer.normalize_from_list(extracted_text_list)
        ans = {}
        ans.setdefault(PE_DICT_NAME_PRICE, [])
        ans.setdefault(PE_DICT_NAME_PPH, [])
        print normalized_text_list
        for normalized in normalized_text_list:
            if not normalized[PE_JSON_NAME_TIME_UNIT]:
                ans[PE_DICT_NAME_PPH].append(normalized[PE_JSON_NAME_PRICE])
            else:
                tunit = DIGPE.re_alphabet.findall(normalized[PE_JSON_NAME_TIME_UNIT])
                if tunit and tunit[0].strip() in UNIT_TIME_HOUR:
                    if tunit[0].strip() in UNIT_TIME_HOUR:
                        digits = DIGPE.re_digits.findall(normalized[PE_JSON_NAME_TIME_UNIT])
                        if not digits or int(digits[0]) == 1:
                            # ans.append(normalized)
                            ans[PE_DICT_NAME_PPH].append(normalized[PE_JSON_NAME_PRICE])

            ans[PE_DICT_NAME_PRICE].append(normalized)
        return ans


    def extract_from_list(self, text_list):
        return [self.extract(text) for text in text_list]

if __name__ == '__main__':
    # text = '$550 1 hr'
    # text = 'Good morning I\'m doing incalls only gentleman I\'m quick 60 roses ?Hhr 80 roses ?Hour 120 roses unrushed and f.service provided nonnegotiable donations  614-563-3342'
    text = 'Short Stay 100 roses'
    digpe = DIGPE()
    print digpe.extract(text)


