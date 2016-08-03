# -*- coding:utf-8 -*-

import re

from yandex_yaca_parser.exceptions import YandexYacaParserError
from yandex_yaca_parser.utils import to_unicode, get_full_domain_without_scheme


class YandexYacaParser(object):
    params_regexr = re.U | re.M | re.DOTALL | re.I

    patterns = {
        'pagecount': re.compile(ur'<div class="info info_before-columns">Найдено сайтов:\s*([^<]+)\s*</div>', params_regexr),
        'title': re.compile(ur'<h2\s*class="yaca-snippet__title">\s*<a[^>]+href="([^"]+)"[^>]*>\s*(.*?)\s*</a>\s*</h2>', params_regexr),
        'descr': re.compile(ur'<div class="yaca-snippet__text">(.*?)</div>', params_regexr),
        'serp': re.compile(ur'<(li|div)\s*class="yaca-snippet">(.*?)</div>\s*</\1>', params_regexr),
        'category': re.compile(ur'<a[^>]+href="(/yaca/cat/[^"]+)"[^>]+>(.*?)</a>', params_regexr),
    }

    def __init__(self, content):
        self.content = to_unicode(content)

    def get_serp(self):
        pagecount = self.get_pagecount()
        snippets = self.get_snippets()
        return {'pc': pagecount, 'sn': snippets}

    def pagination_exists(self):
        return '<div class="pager"' in self.content

    def get_pagecount(self):
        patterns = (
            self.patterns['pagecount'],
        )

        for pattern in patterns:
            match = pattern.search(self.content)
            if match:
                break

        if not match:
            raise YandexYacaParserError(u'Не удалось найти кол-во сайтов')

        return int(re.sub('[^\d]', '', match.group(1)))

    def _get_title(self, sn):
        match = self.patterns['title'].search(sn)
        if not match:
            raise YandexYacaParserError(u'Не удалось найти заголовок')

        u = match.group(1).lower()
        t = match.group(2)
        try:
            d = get_full_domain_without_scheme(u)
        except UnicodeError as e:
            raise e
        return t, u, d

    def _get_descr(self, sn):
        match = self.patterns['descr'].search(sn)
        if not match:
            raise YandexYacaParserError(u'Не удалось найти описание')
        return match.group(1)

    def _get_category(self, sn):
        match = self.patterns['category'].search(sn)
        if match:
            return match.group(1).lower(), match.group(2)
        return '', ''

    def get_snippets(self):
        serp = self.patterns['serp'].findall(self.content)

        snippets = []
        for position, (_, sn) in enumerate(serp):
            t, u, d = self._get_title(sn)
            cu, c = self._get_category(sn)
            snippet = {
                'p': position + 1,
                't': t,
                'u': u,
                'd': d,
                's': self._get_descr(sn),
                'cu': cu,
                'c': c
            }
            snippets.append(snippet)
        return snippets
