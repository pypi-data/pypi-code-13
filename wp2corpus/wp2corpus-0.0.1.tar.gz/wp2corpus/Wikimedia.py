from re import sub, findall


class Wikimedia(object):

    def __init__(self):
        self.placeholder = "<needtobereplaced>"

    def parse(self, input_string):
        input_string = self._remove_comment(input_string)
        input_string = self._remove_heading(input_string)
        input_string = self._remove_link(input_string)
        input_string = self._remove_emphasis(input_string)
        input_string = self._remove_bracket(input_string)
        input_string = self._remove_html_tag(input_string)
        return input_string

    def _remove_comment(self, input_string):
        return sub(r'<!--.*?-->', '', input_string)

    def _remove_heading(self, input_string):
        return sub(r'[\*#]*\s*', '', input_string)
        return input_string

    def _remove_link(self, input_string):
        pat = r'\[+(.*?)\]+'
        res = list(map(lambda s: sub(r'.*\|', '', s),
                       findall(pat, input_string)))
        input_string = sub(r'[\[\{]+(.*?)[\]\}]+',
                           self.placeholder, input_string)

        for res_i in res:
            input_string = input_string.replace(self.placeholder, res_i, 1)

        return input_string

    def _remove_emphasis(self, input_string):
        return sub(r'\'', '', input_string)

    def _remove_bracket(self, input_string):
        return sub(r'[\(（](.*?)[\)）]', '', input_string)

    def _remove_html_tag(self, input_string):
        return sub('<.*\/.*?>', '', input_string)
