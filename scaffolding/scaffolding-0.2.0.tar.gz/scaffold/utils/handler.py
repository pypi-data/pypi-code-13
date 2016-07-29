import os
from subprocess import check_output, CalledProcessError
from template import Template
from config_parser import ConfigParser
from exceptions import FileNotFound, TemplateNotFound


class Converter(object):
    """ Given a directory or file which may containing variables, it should
        be able to return a converted directory or file name
    """
    def __init__(self, path, context):
        self.path = path.rstrip('/')
        self.context = context

    def convert(self):
        base = os.path.basename(self.path)
        template = Template(temp_file=None, temp_str=base)
        base = template.render(self.context)
        return base


class Scaffolder(object):
    def __init__(self, tdir):
        self.tdir = tdir
        self.context = {}

    def list_templates(self):
        for d in os.listdir(self.tdir):
            print d

    def create_layout(self, name, template):
        if name:
            path = os.path.join(self.tdir, name)
            if not os.path.isdir(path):
                raise TemplateNotFound(path)
        elif template:
            path = os.path.expanduser(template)
            if not os.path.isdir(path):
                path = os.path.join(os.getcwd(), template)
                if not os.path.isdir(path):
                    raise TemplateNotFound(template)

        cfg = os.path.join(path, 'context')
        if not os.path.isfile(cfg):
            raise FileNotFound(cfg)

        configs = ConfigParser(cfg).parse()

        for variable, default in configs:
            if default:
                val = raw_input('Set %s (default is %s): ' % (variable, default))
            else:
                val = raw_input('Set %s: ' % variable)
            self.context[variable] = val or default

        self._create(path)

    def _create(self, path):
        """
            Render whatever in "path" to the current working directory
        """
        cwd = os.getcwd()
        for d in os.listdir(path):
            dp = os.path.join(path, d)
            if os.path.isfile(dp) and not dp.endswith('context'):
                filename = Converter(dp, self.context).convert()
                with open(os.path.join(cwd, filename), 'w') as fw:
                    rendered = Template(dp).render(self.context)
                    fw.write(rendered)
            elif os.path.isdir(dp):
                dname = Converter(dp, self.context).convert()
                new_path = os.path.join(cwd, dname)
                os.mkdir(new_path, 0755)
                os.chdir(new_path)
                self._create(dp)
                os.chdir(cwd)

    def show_layout(self, name, template):
        if name:
            path = os.path.join(self.tdir, name)
            if not os.path.isdir(path):
                raise TemplateNotFound(path)
        elif template:
            path = os.path.expanduser(template)
            if not os.path.isdir(path):
                path = os.path.join(os.getcwd(), template)
                if not os.path.isdir(path):
                    raise TemplateNotFound(template)

        print path
        self._list_directory(path, 0)

    def _list_directory(self, path, space):
        for d in os.listdir(path)[::-1]:
            dp = os.path.join(path, d)
            if os.path.isdir(dp):
                print '|' + ' ' * space + '-- ' + d
                self._list_directory(dp, space + 3)
            else:
                print '|' + ' ' * space + '-- ' + d

    def remove(self, name):
        path = os.path.join(self.tdir, name)
        if os.path.isdir(path):
            try:
                check_output(['rm', '-r', path])
            except CalledProcessError, e:
                print e.output

    def install(self, template):
        path = os.path.expanduser(template)
        if not os.path.isdir(path):
            path = os.path.join(os.getcwd(), template)
            if not os.path.isdir(path):
                raise TemplateNotFound(template)

        try:
            check_output(['cp', '-r', path, self.tdir])
        except CalledProcessError, e:
            print e.output

    @property
    def location(self):
        return self.tdir





