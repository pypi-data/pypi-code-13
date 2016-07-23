from re import sub, findall


class Wikimedia(object):

    def __init__(self):
        self.placeholder = "<needtobereplaced>"

    def parse(self, input_string):
        result = list()
        for token in input_string.split():
            token = self._remove_comment(token)
            token = self._remove_heading(token)
            token = self._remove_link(token)
            token = self._remove_emphasis(token)
            token = self._remove_bracket(token)
            token = self._remove_html_tag(token)
            result.append(token)

        return ' '.join(result)

    def _remove_comment(self, token):
        return sub(r'<!--.*?-->', '', token)

    def _remove_heading(self, token):
        return sub(r'[\*#]*\s*', '', token)
        return token

    def _remove_link(self, token):
        pat = r'\[+(.*?)\]+'
        res = list(map(lambda s: sub(r'.*\|', '', s),
                       findall(pat, token)))
        token = sub(r'[\[\{]+(.*?)[\]\}]+',
                           self.placeholder, token)

        for res_i in res:
            token = token.replace(self.placeholder, res_i, 1)

        return token

    def _remove_emphasis(self, token):
        return sub(r'\'', '', token)

    def _remove_bracket(self, token):
        return sub(r'[\(（](.*?)[\)）]', '', token)

    def _remove_html_tag(self, token):
        return sub('<.*\/.*?>', '', token)
