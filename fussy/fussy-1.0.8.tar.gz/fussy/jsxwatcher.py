"""Sample utility script to watch for jsx and es6 file changes and publish to js files

Runs babel across .jsx and .es6 files to generate .js files...

Obviously that's not particularly useful, since babel already
includes "watch" functionality, but the idea is to demonstrate the 
operation.
"""
import os, sys, logging
from fussy import filewatch, nbio
log = logging.getLogger(__name__)
HERE = os.path.dirname(__file__)

def find_static_js_directories(directory):
    for dir, subdirs, files in os.walk( os.path.abspath(directory)):
        if os.path.basename(dir) == 'static':
            if 'js' in subdirs:
                yield os.path.join( dir, 'js' )
    
def process( filename ):
    """Runs babel with jsx and es2015 presets
    
        npm install -g babel-cli babel-preset-react babel-preset-es2015
    """
    final = os.path.splitext( filename )[0] + '.js'
    if final == filename:
        raise RuntimeError("Somehow we got a .js file passed in, which would overwrite it with itself")
    if os.path.exists(final):
        if os.stat(final).st_mtime > os.stat(filename).st_mtime:
            return False
    log.info("  %s",filename)
    command = [
        'babel',
            '--preset',
                'react,es2015',
            '--plugins',
                'transform-class-properties',
            '-o', final,
            '--source-maps', 'inline',
            filename,
    ]
    log.debug("Running: %s", ' '.join(command))
    nbio.Process(command)()
    log.info("    => %s",final)

def main():
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('fussy.filewatch').setLevel( logging.WARN )
    directories = list(find_static_js_directories(sys.argv[1]))
    log.info("Watching directories:\n  %s","\n  ".join(directories))
    fw = filewatch.FileWatcher( directories[0], pattern='*.jsx', recursive=True )
    for directory in directories[1:]:
        fw.on_directory_added( directory )
    for event in fw:
        try:
            process( event.full_name )
        except Exception as err:
            err.args += (event,)
            raise
