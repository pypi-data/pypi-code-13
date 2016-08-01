# coding: utf-8

import os, os.path
import re


class TagHandler(object):
    def __init__(self, ctx=None):
        self.ctx = ctx

    def handle(self, ctx, line):
        raise NotImplementedError()


class IncludeTagHandler(TagHandler):
    def handle(self, line, ctx=None):
        if ctx is None:
            ctx = self.ctx
        filename = line.split()[1].strip()

        ctx.fill_file(os.path.join(os.path.dirname(ctx.current_file), filename))


class ConfigurationContext(object):
    def __init__(self, strict=False):
        self.strict = strict
        self.value = {}
        self.current_file = None

        self._tag_handlers = {
            "include": IncludeTagHandler()
        }

    @staticmethod
    def _resolve_fill_filename(filename):
        return os.path.abspath(filename)

    def fill_line(self, line):
        line = line.strip()
        if len(line) == 0:
            return

        if line.startswith('@'):
            # tag
            self._handle_tag(line)
        elif line.startswith("#"):
            # comment
            pass
        else:
            try:
                key, value = re.split("=|:", line, 1)
                self.value[key.strip()] = value.strip()
            except Exception, e:
                if self.strict:
                    print "line: %s\t" % line, e

        return self

    def add_tag_handler(self, name, tag_handler):
        self._tag_handlers[name] = tag_handler

    def _handle_tag(self, line):
        if len(line) < 2:
            return
        tag_indicator = line[1:].split()[0].strip()
        self._tag_handlers[tag_indicator].handle(line, ctx=self)

    def fill_file(self, filename):
        real_path = self._resolve_fill_filename(filename)
        assert os.path.exists(real_path) and os.path.isfile(real_path), "conf file %s not exist" % real_path
        self.current_file = real_path
        with open(real_path, 'r') as fp:
            for line in fp:
                self.fill_line(line)

        return self

    def _resolve_key_prefix(self, key, prefix):
        if prefix is None:
            return key
        return '%s.%s' % (prefix, key,)

    def get(self, key, default=None, prefix=None):
        return self.value.get(key, default)

    def get_int(self, key, default=None):
        return int(self.get(key, default))

    def get_bool(self, key, default=None):
        value = self.get(key, default)
        if not value:
            return False
        value = value.lower()
        if value == 'false':
            return False
        return True

    def mget(self, *keys, **kw):
        prefix = kw.get("prefix", None)
        values = []
        for key in keys:
            values.append(self.get(self._resolve_key_prefix(key, prefix)))
        return tuple(values)

    def __str__(self):
        return str(self.value)

    __repr__ = __str__


def load_configuration(filename):
    return ConfigurationContext(strict=True).fill_file(filename)


if __name__ == '__main__':
    conf = load_configuration("./conf/prod.properties")
    print conf
