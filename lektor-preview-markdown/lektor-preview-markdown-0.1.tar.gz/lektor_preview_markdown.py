from lektor.pluginsystem import Plugin
from lektor.markdown import Markdown


class PreviewMarkdownPlugin(Plugin):
    name = u'Preview Markdown'
    description = u'Adds filter to trim a Markdown post to a specified length.'

    def on_setup_env(self, **extra):

        def preview(value, length=255, ellipsis='...'):
            if len(value.source) <= length:
                return value
            trimmed = value.source[:length]

            # mid-sentence
            if trimmed[-1] == ' ':
                ret = trimmed.rstrip()
            # end of sentence
            elif trimmed[-1] in '.?!':
                ret = trimmed + ' '
            # mid-word
            else:
                ret = trimmed[:trimmed.rfind(' ')].rstrip()
            return Markdown(ret + ellipsis)

        self.env.jinja_env.filters['preview'] = preview
