# -*- coding: utf-8 -*-
from __future__ import print_function

import epitropos

from malibu import command
from malibu.command import module
from malibu.util import args
from malibu.util import log


def command_main():
    """ Entry point for calling epitropos from the command line.
    """

    arp = args.ArgumentParser.from_argv()
    arp.set_default_param_type(
        arp.PARAM_LONG,
        arp.OPTION_PARAMETERIZED)

    arp.add_option_mapping('D', 'debug')
    arp.add_option_type('D', arp.OPTION_SINGLE)
    arp.add_option_description('D', 'See also: --debug')

    arp.add_option_type('debug', arp.OPTION_SINGLE)
    arp.add_option_description('debug', 'Print noisy logging messages')

    modloader = module.CommandModuleLoader(arp)
    modloader.register_modules(
        command.get_command_modules(package=__package__).values()
    )
    modloader.instantiate_modules()

    arp.parse()

    if len(arp.parameters) < 2:
        arp.parameters.append('help:all')

    try:
        debug = arp.options['debug']
    except:
        debug = False

    epitropos.set_debug(debug)

    # Load logging settings from the configuration module.
    modcfg = modloader.get_module_by_base('config')
    if not modcfg:
        raise module.CommandModuleException('Config module is not loaded.')
    else:
        cfg = modcfg.get_configuration()
        try:
            logcfg = cfg.get_section('logging')
            log.LoggingDriver(
                logfile=logcfg.get_string('logfile', '/tmp/epitropos.log'),
                loglevel=logcfg.get_string('loglevel', 'DEBUG'),
                stream=logcfg.get_bool('console_log', False) or debug,
                name='epitropos').find_logger()
        except Exception as e:
            print(' ==> Exception:', str(e))
            print(' ==> Falling back to logging defaults.')

            # Fallback setup for LoggingDriver
            log.LoggingDriver(
                logfile='/dev/null',
                loglevel='DEBUG',
                stream=True,
                name='epitropos').find_logger()

    modloader.save_state('epitropos')

    modloader.parse_command(
        arp.parameters[1],
        *arp.parameters[1:],
        args=arp)

    modloader.deinit_modules()
