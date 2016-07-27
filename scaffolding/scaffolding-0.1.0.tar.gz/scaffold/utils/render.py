import sys
import re
tag = re.compile('({{.*?}})')


class ContextDoseNotExist(Exception):
    def __init__(self, file='', lineno=0, name=''):
        if file:
            self.message = '%s line %d: {{ %s }} not defined.' % (
                file, lineno, name
            )
        else:
            self.message = '{{ %s }} not defined.' % name


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
                result.append(self._render(token, context, lineno))
                lineno += token[0].count('\n')
        except ContextDoseNotExist, e:
            if self.file:
                print e.message
            else:
                print 'In %s, %s' % (self.template_string, e.message)
            sys.exit(-1)
        return ''.join(result)

    def _render(self, token, context, lineno):
        text, t = token
        if t == 'TEXT':
            return text
        else:
            try:
                return context[text]
            except KeyError:
                raise ContextDoseNotExist(self.file, lineno, text)

    @classmethod
    def _get_template_string(cls, f):
        with open(f, 'r') as temp:
            return temp.read()





