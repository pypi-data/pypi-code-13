#!/usr/bin/env python

from os import listdir, symlink, path, makedirs, path
from distutils.core import setup
from distutils.command.install_scripts import install_scripts
from distutils.command.install_data import install_data
import sys

glade_files = ['stuff/' + filename for filename in listdir('stuff') if filename.endswith('.glade')]

paths = {}

class InstallData(install_data):
    def run(self):
        """
        Take care of installing a link from /usr/share/nautilus-scripts/name
        to the installed script.
        """
        install_data.run( self )

        link_name = 'Upload to Gallery'

        root_dir = self.install_dir
        # No "/local", or nautilus-script(s)-manager wouldn't find it:
        root_dir = root_dir.replace( '/usr/local', '/usr' )
        scripts_dir = path.join(root_dir, 'share/nautilus-scripts')
        link_path = path.join( scripts_dir, link_name )
        exec_path = paths['exec']

        if not path.exists( link_path ):
            if not path.exists(scripts_dir):
                print "creating %s." % scripts_dir
                makedirs(scripts_dir)
            
            # path.exists won't work if link_path exists but is stale.
            if not link_name in listdir( scripts_dir ):
                rel_path = path.relpath( exec_path, path.dirname( link_path ) )
                print "linking %s -> %s" % (link_path, rel_path)
                symlink( rel_path, link_path )
        
        return

class InstallScripts(install_scripts):
    def run(self):
        """
        Just dump somewhere the path of the script.
        """
        
        install_scripts.run( self )
        paths['exec'] = self.get_outputs()[0]

setup(name='Gallery Uploader',
      version='2.4',
      description='Upload pictures and videos to Gallery installations',
      license='GPL',
      author='Pietro Battiston',
      author_email='me@pietrobattiston.it',
      url='http://www.pietrobattiston.it/gallery-uploader',
      scripts=['gallery-uploader'],
      packages=['galleryuploader_lib'],
      data_files=[('share/gallery-uploader/stuff', ['stuff/gallery.svg'] + glade_files),
                  ('share/pixmaps', ['stuff/gallery.svg']),
                  ('share/applications', ['stuff/gallery-uploader.desktop'])]+
                  [('share/locale/'+lang+'/LC_MESSAGES/', ['locale/'+lang+'/LC_MESSAGES/gallery_uploader.mo'] ) for lang in listdir('locale')],
      classifiers=[
                   'Development Status :: 5 - Production/Stable',
                   'Environment :: X11 Applications :: GTK',
                   'Intended Audience :: End Users/Desktop',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python',
                   'Topic :: Internet :: WWW/HTTP',
                   'Topic :: Multimedia :: Graphics',
                   'Topic :: Desktop Environment :: Gnome',
                   'Topic :: Utilities',
                   ],
      cmdclass={'install_data': InstallData,
                'install_scripts': InstallScripts
                }
     )
