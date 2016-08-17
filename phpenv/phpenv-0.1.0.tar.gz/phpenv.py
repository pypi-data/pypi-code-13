#!/usr/bin/env python2.7

import os
import sys
import optparse
import json
import urllib2
import tarfile
import contextlib
import io
import pipes
import subprocess
import stat

__version__ = '0.1.0'

def create_logger():
    pass

@contextlib.contextmanager
def tarfile_open(*args, **kwargs):
    tf = tarfile.open(*args, **kwargs)
    try:
        yield tf
    finally:
        tf.close()

def download_php_src(php_url, src_dir, opt):
    tar_contents = io.BytesIO(urllib2.urlopen(php_url).read())
    with tarfile_open(fileobj=tar_contents) as tarfile_obj:
        tarfile_obj.extractall(src_dir)

def get_php_versions():
    php5 = json.loads(urllib2.urlopen('https://secure.php.net/releases/index.php?json&version=5&max=1000').read().decode('UTF-8'))
    php7 = json.loads(urllib2.urlopen('https://secure.php.net/releases/index.php?json&version=7&max=1000').read().decode('UTF-8'))

    versions = php5.copy()
    versions.update(php7)

    return versions

def print_php_versions():
    versions = get_php_versions()

    version_list = [key for key in versions]
    version_list = sorted(version_list, key=lambda s: [int(u) for u in s.split('.')])

    chunk_of_8 = [
            version_list[pos:pos + 8] for pos in range(0, len(version_list), 8)
    ]

    for chunk in chunk_of_8:
        print '\t'.join(chunk)

def get_latest_php_version(major=7):
    versions = get_php_versions()

    version_list = [key for key in versions if key.split('.')[0] == str(major)]
    version_list = sorted(version_list, key=lambda s: [int(u) for u in s.split('.')])
    
    return version_list.pop()

def find_openssl_dir():

    find = os.popen('find /usr/ -name openssl -type d 2>/dev/null')
    ret = find.read().split("\n")
    openssl_root_dir = None

    for path in ret:
        if os.path.exists(os.path.join(path, 'evp.h')):
            openssl_root_dir = os.path.abspath(os.path.join(path,'..','..'))

    if not openssl_root_dir:
        print " * Openssl not found"
        sys.exit(2)

    if openssl_root_dir == '/usr':
        return None

    return openssl_root_dir


def parse_args():
    
    parser = optparse.OptionParser(
            usage="%prog [OPTIONS] <env_dir>",
            version=__version__)

    parser.add_option('-p', '--python-virtualenv',
            action='store_true', default=False, dest='python_virtualenv',
            help='Use current python virtualenv instead create new')

    parser.add_option('--php', action='store', default='latest',
            dest='php', metavar='PHP_VERSION',
            help='The php version to use')

    parser.add_option('-l', '--list', action='store_true', 
            dest='list', default=False,
            help='List available php versions and exit')

    parser.add_option('--prompt', action='store',
            dest='prompt', default='',
            help='Prompt')


    parser.add_option('-v', '--verbose', action='store_true',
            dest='verbose', default=False,
            help='Verbosity output')

    options, args = parser.parse_args()
    if not options.list and not options.python_virtualenv:
        if not args:
            parser.error('You must provide a <env_dir> or '
                         'use current python virtualenv')
        if len(args) > 1:
            parser.error('There must be only one argument: <env_dir> '
                         '(you gave: {0})'.format(' '.join(args)))
    return options, args

def get_php_src_url(version):
    versions = get_php_versions()
    try:
        filename = versions[version]['source'][1]['filename']
    except KeyError:
        print "Presented version {0} not found".format(version)
        sys.exit(2)
    
    if versions[version].has_key('museum') and versions[version]['museum']:
        return 'http://museum.php.net/php5/{0}'.format(filename)
    else:
        return 'http://php.net/get/{0}/from/this/mirror'.format(filename)
    

def get_env_dir(opt, args):
    if opt.python_virtualenv:
        if hasattr(sys, 'real_prefix'):
            res = sys.prefix
        elif hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix:
            res = sys.prefix
        else:
            print "No python environment is available"
            sys.exit(2)
    else:
        res = args[0]

    return res

def writefile(dest, content, overwrite=True, append=False):

    mode_0755 = (stat.S_IRWXU | stat.S_IXGRP |
                 stat.S_IRGRP | stat.S_IROTH | stat.S_IXOTH)

    if not os.path.exists(dest):
        print " * Writing %s ... " % dest
        with open(dest, 'wb') as f:
            f.write(content)
        os.chmod(dest, mode_0755)
        return
    else:
        with open(dest, 'rb') as f:
            c = f.read()
        if content in c:
            print " * Content %s already in place" % dest
            return

        if not overwrite:
            print ' * File %s exists with different content' % dest
            return

        if append:
            print ' * Appending data to %s' % dest
            with open(dest, 'ab') as f:
                f.write(DISABLE_PROMPT.encode('utf-8'))
                f.write(content.encode('utf-8'))
                f.write(ENABLE_PROMPT.encode('utf-8'))
            return

        print ' * Overwriting %s with new content' % dest
        with open(dest, 'wb') as f:
            f.write(content)



def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print "Directory {0} already exists".format(path)

def callit(cmd, show_stdout=True, in_shell=False, cwd=None):

    all_output = []
    cmd_parts = []

    for part in cmd:
        if len(part) > 45:
            part = part[:20] + "..." + part[-20:]
        if ' ' in part or '\n' in part or '"' in part or "'" in part:
            part = '"%s"' % part.replace('"', '\\"')
        cmd_parts.append(part)
    cmd_desc = ' '.join(cmd_parts)

    print " ** Running command {0}".format(cmd_desc)

    if in_shell:
        cmd = ' '.join(cmd)

    stdout = subprocess.PIPE

    try:
        proc = subprocess.Popen(
                cmd, stderr=subprocess.STDOUT, stdin=None, stdout=stdout,
                cwd=cwd, env=None, shell=in_shell)
    except Exception:
        e = sys.exc_info()[1]
        print "Error {0} while executing command {1}".format(e, cmd_desc)
        raise

    stdout = proc.stdout
    while stdout:
        line = stdout.readline()
        if not line:
            break
        line = line.decode('UTF-8').rstrip()
        all_output.append(line)
        if show_stdout:
            print line
    proc.wait()

    if proc.returncode:
        if show_stdout:
            for s in all_output:
                print s
        raise OSError("Command %s faled with error code %s" % (cmd_desc, proc.returncode))
    return proc.returncode, all_output

def build_php_from_src(env_dir, src_dir, opt):
    conf_cmd = []
    conf_cmd.append('./configure')
    conf_cmd.append('--prefix=%s' % pipes.quote(env_dir))
    conf_cmd.append('--sbindir=%s' % pipes.quote(os.path.join(env_dir,'bin')))
    conf_cmd.append('--mandir=%s' % pipes.quote(os.path.join(env_dir,'share','man')))
    conf_cmd.append('--datadir=%s' % pipes.quote(os.path.join(env_dir,'share')))
    conf_cmd.append('--enable-fpm')
    openssl = find_openssl_dir()
    if openssl:
        conf_cmd.append('--with-openssl=%s' % pipes.quote(openssl))
    else:
        conf_cmd.append('--with-openssl')

        

    #print src_dir

    callit(conf_cmd, opt.verbose, True, src_dir)
    callit(['make'], opt.verbose, True, src_dir)
    callit(['make', 'install'], opt.verbose, True, src_dir)


def install_activate(env_dir, opt):
    files = {'activate': ACTIVATE_SH}

    bin_dir = os.path.join(env_dir, 'bin')
    prompt = opt.prompt or '(%s)' % os.path.basename(os.path.abspath(env_dir))

    for name, content in files.items():
        file_path = os.path.join(bin_dir, name)
        content = content.replace('__PHP_VIRTUAL_PROMPT__', prompt)
        content = content.replace('__PHP_VIRTUAL_ENV__', os.path.abspath(env_dir))
        content = content.replace('__BIN_NAME__', os.path.basename(bin_dir))

        need_append = opt.python_virtualenv

        writefile(file_path, content, append=need_append)

def install_php(env_dir, src_dir, opt):
    env_dir = os.path.abspath(env_dir)

    php_url = get_php_src_url(opt.php)
    download_php_src(php_url, src_dir, opt)
    #print opt
    php_src_dir = os.path.join(src_dir, 'php-{0}'.format(opt.php))

    build_php_from_src(env_dir, php_src_dir, opt)

def install_composer(env_dir, opt):
    composer_content = urllib2.urlopen('https://getcomposer.org/installer').read()

    proc = subprocess.Popen(
            (
                'bash', '-c',
                '. {0} && exec php -- --install-dir={1} --filename=composer'.format(
                    pipes.quote(os.path.join(env_dir, 'bin', 'activate')),
                    pipes.quote(os.path.join(env_dir, 'bin'))
                    )
            ),
            env=os.environ,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
    )
    
    out, _ = proc.communicate(composer_content)
    print out

def create_environment(env_dir, opt):
    if os.path.exists(env_dir) and not opt.python_virtualenv:
        print 'Environment already exists: {0}'.format(env_dir)
        sys.exit(2)

    src_dir = os.path.abspath(os.path.join(env_dir, 'src'))
    mkdir(src_dir)

    install_php(env_dir, src_dir, opt)
    #mkdir(os.path.join(env_dir, 'bin'))
    install_activate(env_dir, opt)
    install_composer(env_dir, opt)

def main():

    opt, args = parse_args()
    #print opt
    #print args

    if opt.list:
        print_php_versions()
        sys.exit(0)

    if opt.php == 'latest':
        opt.php = get_latest_php_version()
    elif opt.php == '5' or opt.php == '7':
        opt.php = get_latest_php_version(opt.php)
    elif int(opt.php.split('.')[0]) < 5:
        print "Php major versions < 5 not supported"
        sys.exit(2)

    #print opt.php
    #print get_php_src_url(opt.php)

    env_dir = get_env_dir(opt, args)
    #print env_dir
    create_environment(env_dir, opt)



# ----------------------------------------------------------------------------
# Shell scripts content

DISABLE_PROMPT = """
PHP_VIRTUAL_ENV_DISABLE_PROMPT=1
"""

ENABLE_PROMPT = """
unset PHP_VIRTUAL_ENV_DISABLE_PROMPT
"""

ACTIVATE_SH = """

deactivate_php () {
    if [ -n "$_OLD_PHP_VIRTUAL_PATH" ] ; then
        PATH="$_OLD_PHP_VIRTUAL_PATH"
        export PATH
        unset _OLD_PHP_VIRTUAL_PATH

        
    fi

    if [ -n "$BASH" -o -n "$ZSH_VERSION" ]; then
        hash -r
    fi

    if [ -n "$_OLD_PHP_VIRTUAL_PS1" ]; then
        PS1="$_OLD_PHP_VIRTUAL_PS1"
        export PS1
        unset _OLD_PHP_VIRTUAL_PS1
    fi

    unset PHP_VIRTUAL_ENV

    if [ ! "$1" = "nondestructive" ]; then
        unset -f deactivate_php
    fi
}

deactivate_php nondestructive

if [ "${BASH_SOURCE[0]}" ]; then
    SOURCE="${BASH_SOURCE[0]}"

    while [ -h "$SOURCE" ]; do SOURCE="$(readlink "$SOURCE")"; done
    DIR="$( command cd -P "$( dirname "$SOURCE" )" > /dev/null && pwd )"

    PHP_VIRTUAL_ENV="$(dirname "$DIR")"
else
    PHP_VIRTUAL_ENV="__PHP_VIRTUAL_ENV__"
fi

export PHP_VIRTUAL_ENV

_OLD_PHP_VIRTUAL_PATH=""$PATH
PATH="$PHP_VIRTUAL_ENV/__BIN_NAME__:$PATH"
export PATH

if [ -z "$PHP_VIRTUAL_ENV_DISABLE_PROMPT" ]; then
    _OLD_PHP_VIRTUAL_PS1="$PS1"
    if [ "x__PHP_VIRTUAL_PROMPT__" != x ]; then
        PS1="__PHP_VIRTUAL_PROMPT__$PS1"
    else
        if [ "`basename \"$PHP_VIRTUAL_ENV\"`" = "__" ]; then
            PS1="[`basename \`dirname \"$PHP_VIRTUAL_ENV\"\``] $PS1"
        else
            PS1="(`basename \"$PHP_VIRTUAL_ENV\"`)$PS1"
        fi
    fi
    export PS1
fi

if [ -n "$BASH" -o -n "$ZSH_VERSION" ]; then
    hash -r
fi
"""
if __name__ == '__main__':
    main()
