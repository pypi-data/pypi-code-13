import sys
import os.path

# make sure this is run from inside the package
from . import config as mimodd_settings
from . import FileAccessError


class GalaxyAccess (object):
    CONFIG_FILE_GUESSES = ['config/galaxy.ini',
                           'universe_wsgi.ini']
    TOOL_CONFIG_FILE_REF = 'tool_config_file'
    pkg_galaxy_data_path = os.path.join(
        os.path.dirname(mimodd_settings.__file__),
        'galaxy_data')
    tool_conf_file = os.path.join(
        pkg_galaxy_data_path,
        'mimodd_tool_conf.xml')

    @classmethod
    def set_toolbox_path (cls):
        """Update the mimodd_tool_conf.xml file installed as part of the
        package with an absolute tool_path to the package xml wrappers."""
        
        with open(cls.tool_conf_file, 'r', encoding='utf-8') as sample:
            template = sample.readlines()[1:]
        with open(cls.tool_conf_file, 'w', encoding='utf-8') as out:
            out.write('<toolbox tool_path="{0}">\n'
                      .format(cls.pkg_galaxy_data_path)
                      )
            out.writelines(template)

    def __init__ (self, galaxydir = None, config_file = None):
        if galaxydir is None and config_file is None:
            raise ArgumentParseError(
                'The location of either the Galaxy root directory '
                'or of the Galaxy config file must be specified.'
                )
        if galaxydir and not os.path.isdir(galaxydir):
            raise FileAccessError(
                '{0} does not seem to be a valid directory.'
                .format(galaxydir)
                )
        # TO DO: see if we can reliably determine the Galaxy root directory
        # from the specified config_file in at least some situations.
        # Right now, we simply store the passed in value even if that is None.
        self.galaxy_dir = galaxydir
        if config_file is None:
            self.config_file = self.get_config_file()
        else:
            self.config_file = config_file
        with open(self.config_file, 'r', encoding='utf-8') as config_in:
            self.config_data = config_in.readlines()

    def get_config_file (self):
        for location_guess in self.CONFIG_FILE_GUESSES:
            config_file = os.path.join(self.galaxy_dir, location_guess)
            if os.path.isfile(config_file):
                return config_file
        raise FileAccessError(
            'Could not find any Galaxy configuration file in its '
            'default location.\n'
            'Please specify the configuration file directly.'
            )

    def add_to_galaxy (self, line_token = None, force = False):
        """Register MiModD's tool wrappers for Galaxy.

        Updates the Galaxy configuration file to include the MiModD
        tool_conf.xml as a tool_config_file.
        """
        
        if line_token is None:
            line_token = self.TOOL_CONFIG_FILE_REF
        value, line_no = self.get_setting(line_token)
        conf_files = [file.strip() for file in value.split(',')]
        if self.tool_conf_file in conf_files:
            print('Galaxy is already configured correctly. No changes needed.')
            return
        self.config_data[line_no] = '{0},{1}\n'.format(
            self.config_data[line_no].rstrip(),
            self.tool_conf_file
            )
        
        # ask for user backup before making changes to Galaxy config file
        print('We recommend to back up the Galaxy configuration file {0} '
              'before proceeding!'
              .format(self.config_file)
              )
        confirm = input('Proceed (y/n)? ')
        if confirm != 'y' and confirm != 'Y':
            print('No changes made to Galaxy configuration file. Aborting.')
            return

        # write changes to config file    
        with open(self.config_file, 'w', encoding='utf-8') as config_out:
            try:
                config_out.writelines(self.config_data)
            except:
                raise OSError(
                    'We are very sorry, but an error has occurred while '
                    'making changes to the Galaxy configuration file {0}. '
                    'If you have made a backup of the file, you may want '
                    'to use it now.'
                    .format(self.config_file)
                    )
                
        print('Successfully updated the Galaxy configuration file {0} '
              'to include the MiModD tools.'
              .format(self.config_file)
              )
        print('If Galaxy is currently running, you will have to restart it '
              'for changes to take effect.'
              )

    def get_setting (self, token):
        for line_no, line in enumerate(self.config_data):
            if line.startswith(token):
                try:
                    key, value = line.split('=')
                except ValueError:
                    raise OSError(
                        'Unexpected format of configuration file line {0}: {1}.'
                        .format(line_no, line)
                        )
                key = key.rstrip()
                if key == token:
                    value = value.strip()
                    return value, line_no
        raise OSError(
            'Galaxy configuration file {0} has no {1} setting. '
            'Maybe the line "{1} = ..." has been commented out?'
            .format(self.config_file, token)
            )
                
        
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        usage=argparse.SUPPRESS,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='\nintegrate this installation of MiModD into '
                    'a local Galaxy.\n'
        )
    parser.add_argument(
        'galaxyhook',
        metavar='GALAXY_PATH',
        help="path to your local Galaxy's root directory "
             'or to its galaxy.ini configuration file '
             '(use the later if the tool fails to autodetect '
             'the config file from the given root directory).'
        )
    parser.add_argument(
        '-t', '--token',
        dest='line_token',
        default=argparse.SUPPRESS,
        help='add the path to the MiModD Galaxy tool wrappers to this variable '
             'in the configuration file (default: tool_config_file)'
        )
    args = vars(parser.parse_args())
    # If the positional argument is a directory name, we treat it as the
    # Galaxy root directory. Otherwise, we assume it is the name of Galaxy's
    # configuration file. Further checks are left to the GalaxyAccess instance.
    if os.path.isdir(args['galaxyhook']):
        GalaxyAccess(galaxydir=args['galaxyhook']
                     ).add_to_galaxy(args.get('line_token'))
    else:
        GalaxyAccess(config_file=args['galaxyhook']
                     ).add_to_galaxy(args.get('line_token'))
