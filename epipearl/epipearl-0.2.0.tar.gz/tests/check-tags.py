# -*- coding: utf-8 -*-

import os

from bs4 import BeautifulSoup

cwd = os.getcwd()

if __name__ == "__main__":

    def check_singlevalue_checkbox(tag_id):
        def f(tag):
            return tag.has_attr('id') and \
                    tag['id'] == tag_id and \
                    tag.has_attr('checked')
        return f

    def check_input_id_value(tag_id, value):
        def f(tag):
            return tag.has_attr('id') and \
                    tag['id'] == tag_id and \
                    tag['value'] == value
        return f


    filename = os.path.join(cwd, 'xuxu.html')
    data = ''
    with open(filename, 'r') as myfile:
        data = myfile.read()

    soup = BeautifulSoup(data, 'html.parser')
    tags = soup.find_all(check_input_id_value(
        tag_id='epiScreenTimeout', value='456'))
    if not tags:
        print 'not found'
    else:
        print 'all fine'
