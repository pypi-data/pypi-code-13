import os
import re
import sys
from alembic import config as alembic_config
from alembic import util
try:
    from alembic.util.compat import SafeConfigParser
except ImportError:
    from alembic.compat import SafeConfigParser
from paste.deploy.loadwsgi import NicerConfigParser
from logging import config as logging_config

class EvenNicerConfigParser(NicerConfigParser):
    def __init__(self, *args, **kwargs):
        NicerConfigParser.__init__(self, *args, **kwargs)
        self._sections_processed = {}

    def get(self, section, option, raw=False, vars=None, fallback=None):
        self._populate_with_variable_assignments(section)
        if sys.version_info < (3, 0):
            return NicerConfigParser.get(self, section, option, raw=raw, vars=vars)
        else:
            return NicerConfigParser.get(self, section, option, raw=raw, vars=vars, fallback=fallback)

    def items(self, section, raw=False, vars=None):
        self._populate_with_variable_assignments(section)
        return NicerConfigParser.items(self, section, raw=raw, vars=vars)

    def options(self, section):
        self._populate_with_variable_assignments(section)
        return NicerConfigParser.options(self, section)

    def remove_section(self, section):
        if section in self._sections_processed:
            del self._sections_processed[section]
        return NicerConfigParser.remove_section(self, section)

    def _populate_with_variable_assignments(self, section):
        if section == 'DEFAULT' or section in self._sections_processed:
            return
        defaults = self.defaults()
        global_vars = dict(defaults)
        self._sections_processed[section] = global_vars
        get_from_globals = {}
        for option in self.options(section):
            if option.startswith('set '):
                name = option[4:].strip()
                global_vars[name] = NicerConfigParser.get(self, section, option)
            elif option.startswith('get '):
                name = option[4:].strip()
                get_from_globals[name] = NicerConfigParser.get(self, section, option)
            else:
                if option in defaults:
                    # @@: It's a global option (?), so skip it
                    continue
                get_from_globals.pop(option, None)
        for lhs, rhs in get_from_globals.items():
            self.set(section, lhs, global_vars[rhs])


class PasteSupportedConfig(alembic_config.Config):
    @util.memoized_property
    def file_config(self):
        if self.config_file_name:
            file_config = EvenNicerConfigParser(self.config_file_name, defaults=self.config_defaults)
            file_config.read(self.config_file_name)
        else:
            file_config = SafeConfigParser(self.config_defaults)
            file_config.add_section(self.config_ini_section)
        if self.config_args:
            for key, value in self.config_args.items():
                # default values are not overwritten
                if key in file_config._defaults:
                    continue
                file_config._defaults[file_config.optionxform(key)] = value
        return file_config

    def update_defaults(self, new_defaults, overwrite=True):
        for key, value in iteritems(new_defaults):
            if not overwrite and key in self.parser._defaults:
                continue
            self.parser._defaults[key] = value

    @util.memoized_property
    def config_defaults(self):
        if self.config_file_name:
            here = os.path.abspath(os.path.dirname(self.config_file_name))
            file__ = os.path.abspath(self.config_file_name)
        else:
            here = ''
            file__ = ''
        return {'here': here, '__file__': file__}

class PasteSupportedCommandLine(alembic_config.CommandLine):
    def main(self, argv=None, setup_logging=False):
        self.parser.add_argument('--paste-global', action='append',
                                 help="Define a variable passed to as "
                                 "global_conf, in the form 'var=value'")
        options = self.parser.parse_args(argv)
        if not hasattr(options, "cmd"):
            self.parser.error("too few arguments")
        else:
            if options.paste_global:
                config_args = {
                    pair[0]: pair[1] if len(pair) > 1 else ''
                    for pair in (
                        [p.strip().replace('\\=', '=') for p in re.split(r'(?<!\\)=', arg, 1)]
                        for arg in options.paste_global
                        )
                    }
            else:
                config_args = {}
            cfg = PasteSupportedConfig(
                file_=options.config,
                ini_section=options.name,
                cmd_opts=options,
                config_args=config_args,
                )
            if setup_logging:
                logging_config.fileConfig(
                    cfg.config_file_name,
                    cfg.config_defaults
                    )
            self.run_cmd(cfg, options)

def main(argv=None, prog=None, **kwargs):
    PasteSupportedCommandLine(prog=prog).main(argv=argv, setup_logging=True)
