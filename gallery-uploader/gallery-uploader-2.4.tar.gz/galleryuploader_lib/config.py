import sys, os
from os import path
from xdg.BaseDirectory import xdg_config_home

########################## CONFIGURATION #######################################

script_path = path.realpath( path.join( sys.path[0], sys.argv[0] ) )

not_installed_dir = path.dirname( script_path )


STUFF_DIR = LOCALE_DIR = None

if path.exists( path.join( not_installed_dir, 'stuff', 'gallery.svg' ) ):
    STUFF_DIR = path.join( not_installed_dir, 'stuff' )
if path.exists( path.join( not_installed_dir, 'locale' ) ):
    LOCALE_DIR = path.join( not_installed_dir, 'locale' )
else:
    for directory in [sys.prefix, path.join( sys.prefix, 'local' )]:
        installed_root_dir = path.join( directory, 'share' )
        if path.exists( path.join( installed_root_dir, 'gallery-uploader', 'stuff', 'gallery.svg' ) ):
            LOCALE_DIR = path.join( installed_root_dir, 'locale' )
            if not STUFF_DIR:
                STUFF_DIR = path.join( installed_root_dir, 'gallery-uploader', 'stuff' )
            break

# Note: no reasonable setup can have "locale" and not "stuff".

from ConfigParser import ConfigParser, NoOptionError

CONFIG_DIR = path.join( xdg_config_home, 'gallery-uploader' )
CONFIG_PATH = path.join( CONFIG_DIR, 'config.ini' )
PROFILES_PATH = path.join( CONFIG_DIR, 'profiles.ini' )

if not path.exists( CONFIG_DIR ):
    # There _is not_ a new config
    
    os.mkdir( CONFIG_DIR )
    print "created", CONFIG_DIR
    
    # Is there an old config?
    old_config_dir = path.expanduser( '~/.gup' )
    old_config_path = path.join( old_config_dir, 'config.ini' )
    if path.exists( old_config_path ):
        # Yes... migrate!
        
        old_profiles = open( old_config_path )
        profiles = old_profiles.read()
        old_profiles.close()

        new_profiles = open( PROFILES_PATH, 'w' )
        new_profiles.write( profiles )
        new_profiles.close()
        
        readme = open( path.join( old_config_dir, 'README' ), 'w' )
        readme.write( """This directory may have been created by a past version of gallery uploader.
If you do not use the "gup" library directly, you can now safely delete it,
since all profiles informations were transferred in
%s.""" % PROFILES_PATH )
        readme.close()
        
profiles = ConfigParser()
profiles.read( [PROFILES_PATH] )

config = ConfigParser()
config.read( [CONFIG_PATH] )

########################## END OF CONFIGURATION ################################


########################## LOCALIZATION ########################################

import locale
import gettext

APP = 'gallery_uploader'

gettext.install(APP, localedir=LOCALE_DIR, unicode=True)

# For gtk.Builders:
locale.bindtextdomain(APP, LOCALE_DIR)

########################## END OF LOCALIZATION #################################

