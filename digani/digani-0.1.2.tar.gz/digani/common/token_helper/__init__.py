# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-13 15:39:38
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-18 14:51:19

from crf_tokenizer import CrfTokenizer

tokenizer = CrfTokenizer()
tokenizer.setRecognizePunctuation(True)
tokenizer.setRecognizeHtmlEntities(True)
tokenizer.setRecognizeHtmlTags(True)
tokenizer.setSkipHtmlTags(False)

import re
re_split = re.compile(r'[\s,]')

def tokenize(content):
    tokens = tokenizer.tokenize(content)
    tokens = re_split.split(' '.join(tokens))
    return ' '.join(tokens)

if __name__ == '__main__':
    # content = '<div class="addthis_toolbox addthis_default_style " addthis: INSTANT SUGAR MUMMY/SUGAR DADDY/GAY AND LESBIAN CONNECTIONS.08166496530." > Post#10172285'
    content = '<a href="http://www.anunico.sg/941-central_region.html" title="Free classifieds in Central Region" >Central Region <a href="http://www.anunico.sg/942-east_region.html" title="Free classifieds in East Region" >East Region <a href="http://www.anunico.sg/943-north_region.html" title="Free classifieds in North Region" >North Region <a href="http://www.anunico.sg/944-north_east_region.html" title="Free classifieds in North-East Region" >North-East Region <a href="http://www.anunico.sg/945-west_region.html" title="Free classifieds in West Region" >West Region'
    print tokenize(content)