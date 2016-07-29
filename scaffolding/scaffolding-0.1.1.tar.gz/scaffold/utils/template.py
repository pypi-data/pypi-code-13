import re
from exceptions import ContextDoseNotExist

tag = re.compile('({{.*?}})')


class Template(object):
    def __init__(self, temp_file, temp_str=''):
        self.file = temp_file
        self.template_string = temp_str or self._get_template_string(self.file)
        self.tokens = self.tokenize()

    def tokenize(self):
        tokens = tag.split(self.template_string)
        result = []
        for token in tokens:
            if token.startswith('{{'):
                result.append((token[2:-2].strip(), 'VAR'))
            else:
                result.append((token, 'TEXT'))
        return result

    def render(self, context):
        result = []
        lineno = 1
        try:
            for token in self.tokens:
                result.append(self._render(token, context))
                lineno += token[0].count('\n')
        except KeyError:
            if self.file:
                raise ContextDoseNotExist(self.file, lineno, token[0])
            else:
                raise ContextDoseNotExist(tstring=self.template_string, name=token[0])
        return ''.join(result)

    @classmethod
    def _render(cls, token, context):
        text, t = token
        if t == 'TEXT':
            return text
        else:
            return context[text]

    @classmethod
    def _get_template_string(cls, f):
        with open(f, 'r') as temp:
            return temp.read()





