"""Amalgamation of xonsh.completers package, made up of the following modules, in order:

* bash
* completer
* pip
* tools
* _aliases
* commands
* man
* path
* python
* base
* dirs
* init

"""

from sys import modules as _modules
from types import ModuleType as _ModuleType
from importlib import import_module as _import_module


class _LazyModule(_ModuleType):

    def __init__(self, pkg, mod, asname=None):
        '''Lazy module 'pkg.mod' in package 'pkg'.'''
        self.__dct__ = {
            'loaded': False,
            'pkg': pkg,  # pkg
            'mod': mod,  # pkg.mod
            'asname': asname,  # alias
            }

    @classmethod
    def load(cls, pkg, mod, asname=None):
        if mod in _modules:
            key = pkg if asname is None else mod
            return _modules[key]
        else:
            return cls(pkg, mod, asname)

    def __getattribute__(self, name):
        if name == '__dct__':
            return super(_LazyModule, self).__getattribute__(name)
        dct = self.__dct__
        mod = dct['mod']
        if dct['loaded']:
            m = _modules[mod]
        else:
            m = _import_module(mod)
            glbs = globals()
            pkg = dct['pkg']
            asname = dct['asname']
            if asname is None:
                glbs[pkg] = m = _modules[pkg]
            else:
                glbs[asname] = m
            dct['loaded'] = True
        return getattr(m, name)

#
# bash
#
os = _LazyModule.load('os', 'os')
re = _LazyModule.load('re', 're')
shlex = _LazyModule.load('shlex', 'shlex')
pickle = _LazyModule.load('pickle', 'pickle')
hashlib = _LazyModule.load('hashlib', 'hashlib')
pathlib = _LazyModule.load('pathlib', 'pathlib')
builtins = _LazyModule.load('builtins', 'builtins')
subprocess = _LazyModule.load('subprocess', 'subprocess')
xl = _LazyModule.load('xonsh', 'xonsh.lazyasd', 'xl')
xp = _LazyModule.load('xonsh', 'xonsh.platform', 'xp')
RE_DASHF = xl.LazyObject(lambda: re.compile(r'-F\s+(\w+)'),
                         globals(), 'RE_DASHF')

INITED = False

BASH_COMPLETE_HASH = None
BASH_COMPLETE_FUNCS = {}
BASH_COMPLETE_FILES = {}

CACHED_HASH = None
CACHED_FUNCS = None
CACHED_FILES = None

BASH_COMPLETE_SCRIPT = """source "{filename}"
COMP_WORDS=({line})
COMP_LINE={comp_line}
COMP_POINT=${{#COMP_LINE}}
COMP_COUNT={end}
COMP_CWORD={n}
{func} {cmd} {prefix} {prev}
for ((i=0;i<${{#COMPREPLY[*]}};i++)) do echo ${{COMPREPLY[i]}}; done
"""


def update_bash_completion():
    global BASH_COMPLETE_FUNCS, BASH_COMPLETE_FILES, BASH_COMPLETE_HASH
    global CACHED_FUNCS, CACHED_FILES, CACHED_HASH, INITED

    completers = builtins.__xonsh_env__.get('BASH_COMPLETIONS', ())
    BASH_COMPLETE_HASH = hashlib.md5(repr(completers).encode()).hexdigest()

    datadir = builtins.__xonsh_env__['XONSH_DATA_DIR']
    cachefname = os.path.join(datadir, 'bash_completion_cache')

    if not INITED:
        if os.path.isfile(cachefname):
            # load from cache
            with open(cachefname, 'rb') as cache:
                CACHED_HASH, CACHED_FUNCS, CACHED_FILES = pickle.load(cache)
                BASH_COMPLETE_HASH = CACHED_HASH
                BASH_COMPLETE_FUNCS = CACHED_FUNCS
                BASH_COMPLETE_FILES = CACHED_FILES
        else:
            # create initial cache
            _load_bash_complete_funcs()
            _load_bash_complete_files()
            CACHED_HASH = BASH_COMPLETE_HASH
            CACHED_FUNCS = BASH_COMPLETE_FUNCS
            CACHED_FILES = BASH_COMPLETE_FILES
            with open(cachefname, 'wb') as cache:
                val = (CACHED_HASH, CACHED_FUNCS, CACHED_FILES)
                pickle.dump(val, cache)
        INITED = True

    invalid = ((not os.path.isfile(cachefname)) or
               BASH_COMPLETE_HASH != CACHED_HASH or
               _completions_time() > os.stat(cachefname).st_mtime)

    if invalid:
        # update the cache
        _load_bash_complete_funcs()
        _load_bash_complete_files()
        CACHED_HASH = BASH_COMPLETE_HASH
        CACHED_FUNCS = BASH_COMPLETE_FUNCS
        CACHED_FILES = BASH_COMPLETE_FILES
        with open(cachefname, 'wb') as cache:
            val = (CACHED_HASH, BASH_COMPLETE_FUNCS, BASH_COMPLETE_FILES)
            pickle.dump(val, cache)


def complete_from_bash(prefix, line, begidx, endidx, ctx):
    """Completes based on results from BASH completion."""
    update_bash_completion()
    splt = line.split()
    cmd = splt[0]
    func = BASH_COMPLETE_FUNCS.get(cmd, None)
    fnme = BASH_COMPLETE_FILES.get(cmd, None)
    if func is None or fnme is None:
        return set()
    idx = n = 0
    for n, tok in enumerate(splt):
        if tok == prefix:
            idx = line.find(prefix, idx)
            if idx >= begidx:
                break
        prev = tok
    if len(prefix) == 0:
        prefix = '""'
        n += 1
    else:
        prefix = shlex.quote(prefix)

    script = BASH_COMPLETE_SCRIPT.format(
        filename=fnme, line=' '.join(shlex.quote(p) for p in splt),
        comp_line=shlex.quote(line), n=n, func=func, cmd=cmd,
        end=endidx + 1, prefix=prefix, prev=shlex.quote(prev))
    try:
        out = subprocess.check_output(
            [xp.bash_command()], input=script, universal_newlines=True,
            stderr=subprocess.PIPE, env=builtins.__xonsh_env__.detype())
    except (subprocess.CalledProcessError, FileNotFoundError):
        out = ''

    rtn = set(out.splitlines())
    return rtn


def _load_bash_complete_funcs():
    global BASH_COMPLETE_FUNCS
    BASH_COMPLETE_FUNCS = bcf = {}
    inp = _collect_completions_sources()
    if not inp:
        return
    inp.append('complete -p\n')
    out = _source_completions(inp)
    for line in out.splitlines():
        head, _, cmd = line.rpartition(' ')
        if len(cmd) == 0 or cmd == 'cd':
            continue
        m = RE_DASHF.search(head)
        if m is None:
            continue
        bcf[cmd] = m.group(1)


def _load_bash_complete_files():
    global BASH_COMPLETE_FILES
    inp = _collect_completions_sources()
    if not inp:
        BASH_COMPLETE_FILES = {}
        return
    if BASH_COMPLETE_FUNCS:
        inp.append('shopt -s extdebug')
        bash_funcs = set(BASH_COMPLETE_FUNCS.values())
        inp.append('declare -F ' + ' '.join([f for f in bash_funcs]))
        inp.append('shopt -u extdebug\n')
    out = _source_completions(inp)
    func_files = {}
    for line in out.splitlines():
        parts = line.split()
        if xp.ON_WINDOWS:
            parts = [parts[0], ' '.join(parts[2:])]
        func_files[parts[0]] = parts[-1]
    BASH_COMPLETE_FILES = {
        cmd: func_files[func]
        for cmd, func in BASH_COMPLETE_FUNCS.items()
        if func in func_files
    }


def _source_completions(source):
    try:
        return subprocess.check_output(
            [xp.bash_command()], input='\n'.join(source),
            universal_newlines=True, env=builtins.__xonsh_env__.detype(),
            stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        return ''


def _collect_completions_sources():
    sources = []
    completers = builtins.__xonsh_env__.get('BASH_COMPLETIONS', ())
    paths = (pathlib.Path(x) for x in completers)
    for path in paths:
        if path.is_file():
            sources.append('source "{}"'.format(path.as_posix()))
        elif path.is_dir():
            for _file in (x for x in path.glob('*') if x.is_file()):
                sources.append('source "{}"'.format(_file.as_posix()))
    return sources


def _completions_time():
    compfiles = builtins.__xonsh_env__.get('BASH_COMPLETIONS', ())
    compfiles = [os.stat(x).st_mtime for x in compfiles if os.path.exists(x)]
    return max(compfiles) if compfiles else 0

#
# completer
#
# amalgamated builtins
def complete_completer(prefix, line, start, end, ctx):
    """
    Completion for "completer"
    """
    args = line.split(' ')
    if len(args) == 0 or args[0] != 'completer':
        return None
    curix = args.index(prefix)
    compnames = set(builtins.__xonsh_completers__.keys())
    if curix == 1:
        possible = {'list', 'help', 'add', 'remove'}
    elif curix == 2:
        if args[1] == 'help':
            possible = {'list', 'add', 'remove'}
        elif args[1] == 'remove':
            possible = compnames
        else:
            raise StopIteration
    else:
        if args[1] != 'add':
            raise StopIteration
        if curix == 3:
            possible = {i
                        for i, j in builtins.__xonsh_ctx__.items()
                        if callable(j)}
        elif curix == 4:
            possible = ({'start', 'end'} |
                        {'>' + n for n in compnames} |
                        {'<' + n for n in compnames})
        else:
            raise StopIteration
    return {i for i in possible if i.startswith(prefix)}

#
# pip
#
# amalgamated re
# amalgamated subprocess
# amalgamated xonsh.lazyasd
PIP_RE = xl.LazyObject(lambda: re.compile("pip(?:\d|\.)*"),
                       globals(), 'PIP_RE')
PIP_LIST_RE = xl.LazyObject(lambda: re.compile("pip(?:\d|\.)* (?:uninstall|show)"),
                            globals(), 'PIP_LIST_RE')


@xl.lazyobject
def ALL_COMMANDS():
    try:
        help_text = str(subprocess.check_output(['pip', '--help'],
                                                stderr=subprocess.DEVNULL))
    except FileNotFoundError:
        return []
    commands = re.findall("  (\w+)  ", help_text)
    return [c for c in commands if c not in ['completion', 'help']]


def complete_pip(prefix, line, begidx, endidx, ctx):
    """Completes python's package manager pip"""
    line_len = len(line.split())
    if (line_len > 3) or (line_len > 2 and line.endswith(' ')) or \
                         (not PIP_RE.search(line)):
        return
    if PIP_LIST_RE.search(line):
        try:
            items = subprocess.check_output(['pip', 'list'],
                                            stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            return set()
        items = items.decode('utf-8').splitlines()
        return set(i.split()[0] for i in items)

    if (line_len > 1 and line.endswith(' ')) or line_len > 2:
        # "pip show " -> no complete (note space)
        return
    if prefix not in ALL_COMMANDS:
        suggestions = [c for c in ALL_COMMANDS if c.startswith(prefix)]
        if suggestions:
            return suggestions, len(prefix)
    return ALL_COMMANDS, len(prefix)

#
# tools
#
"""Xonsh completer tools."""
# amalgamated builtins
textwrap = _LazyModule.load('textwrap', 'textwrap')
def _filter_normal(s, x):
    return s.startswith(x)


def _filter_ignorecase(s, x):
    return s.lower().startswith(x.lower())


def get_filter_function():
    """
    Return an appropriate filtering function for completions, given the valid
    of $CASE_SENSITIVE_COMPLETIONS
    """
    csc = builtins.__xonsh_env__.get('CASE_SENSITIVE_COMPLETIONS')
    if csc:
        return _filter_normal
    else:
        return _filter_ignorecase


def justify(s, max_length, left_pad=0):
    """
    Re-wrap the string s so that each line is no more than max_length
    characters long, padding all lines but the first on the left with the
    string left_pad.
    """
    txt = textwrap.wrap(s, width=max_length, subsequent_indent=' '*left_pad)
    return '\n'.join(txt)

#
# _aliases
#
# amalgamated builtins
collections = _LazyModule.load('collections', 'collections')
# amalgamated xonsh.lazyasd
# amalgamated xonsh.completers.tools
VALID_ACTIONS = xl.LazyObject(lambda: frozenset({'add', 'remove', 'list'}),
                              globals(), 'VALID_ACTIONS')


def _add_one_completer(name, func, loc='end'):
    new = collections.OrderedDict()
    if loc == 'start':
        new[name] = func
        for (k, v) in builtins.__xonsh_completers__.items():
            new[k] = v
    elif loc == 'end':
        for (k, v) in builtins.__xonsh_completers__.items():
            new[k] = v
        new[name] = func
    else:
        direction, rel = loc[0], loc[1:]
        found = False
        for (k, v) in builtins.__xonsh_completers__.items():
            if rel == k and direction == '<':
                new[name] = func
                found = True
            new[k] = v
            if rel == k and direction == '>':
                new[name] = func
                found = True
        if not found:
            new[name] = func
    builtins.__xonsh_completers__.clear()
    builtins.__xonsh_completers__.update(new)


def _list_completers(args, stdin=None):
    o = "Registered Completer Functions: \n"
    _comp = builtins.__xonsh_completers__
    ml = max((len(i) for i in _comp), default=0)
    _strs = []
    for c in _comp:
        if _comp[c].__doc__ is None:
            doc = 'No description provided'
        else:
            doc = ' '.join(_comp[c].__doc__.split())
        doc = justify(doc, 80, ml + 3)
        _strs.append('{: >{}} : {}'.format(c, ml, doc))
    return o + '\n'.join(_strs) + '\n'


def _remove_completer(args, stdin=None):
    err = None
    if len(args) != 1:
        err = "completer remove takes exactly 1 argument."
    else:
        name = args[0]
        if name not in builtins.__xonsh_completers__:
            err = ("The name %s is not a registered "
                   "completer function.") % name
    if err is None:
        del builtins.__xonsh_completers__[name]
        return
    else:
        return None, err + '\n', 1


def _register_completer(args, stdin=None):
    err = None
    if len(args) not in {2, 3}:
        err = ("completer add takes either 2 or 3 arguments.\n"
               "For help, run:  completer help add")
    else:
        name = args[0]
        func = args[1]
        if name in builtins.__xonsh_completers__:
            err = ("The name %s is already a registered "
                   "completer function.") % name
        else:
            if func in builtins.__xonsh_ctx__:
                if not callable(builtins.__xonsh_ctx__[func]):
                    err = "%s is not callable" % func
            else:
                err = "No such function: %s" % func
    if err is None:
        position = "start" if len(args) == 2 else args[2]
        func = builtins.__xonsh_ctx__[func]
        _add_one_completer(name, func, position)
    else:
        return None, err + '\n', 1


def completer_alias(args, stdin=None):
    err = None
    if len(args) == 0 or args[0] not in (VALID_ACTIONS | {'help'}):
        err = ('Please specify an action.  Valid actions are: '
               '"add", "remove", "list", or "help".')
    elif args[0] == 'help':
        if len(args) == 1 or args[1] not in VALID_ACTIONS:
            return ('Valid actions are: add, remove, list.  For help with a '
                    'specific action, run: completer help ACTION\n')
        elif args[1] == 'add':
            return COMPLETER_ADD_HELP_STR
        elif args[1] == 'remove':
            return COMPLETER_REMOVE_HELP_STR
        elif args[1] == 'list':
            return COMPLETER_LIST_HELP_STR

    if err is not None:
        return None, err + '\n', 1

    if args[0] == 'add':
        func = _register_completer
    elif args[0] == 'remove':
        func = _remove_completer
    elif args[0] == 'list':
        func = _list_completers
    return func(args[1:], stdin=stdin)

COMPLETER_LIST_HELP_STR = """completer list: ordered list the active completers

Usage:
    completer remove
"""

COMPLETER_REMOVE_HELP_STR = """completer remove: removes a completer from xonsh

Usage:
    completer remove NAME

NAME is a unique name of a completer (run "completer list" to see the current
     completers in order)
"""

COMPLETER_ADD_HELP_STR = """completer add: adds a new completer to xonsh

Usage:
    completer add NAME FUNC [POS]

NAME is a unique name to use in the listing (run "completer list" to see the
     current completers in order)

FUNC is the name of a completer function to use.  This should be a function
     of the following arguments, and should return a set of valid completions
     for the given prefix.  If this completer should not be used in a given
     context, it should return an empty set or None.

     Arguments to FUNC:
       * prefix: the string to be matched
       * line: a string representing the whole current line, for context
       * begidx: the index at which prefix starts in line
       * endidx: the index at which prefix ends in line
       * ctx: the current Python environment

     If the completer expands the prefix in any way, it should return a tuple
     of two elements: the first should be the set of completions, and the
     second should be the length of the modified prefix (for an example, see
     xonsh.completers.path.complete_path).

POS (optional) is a position into the list of completers at which the new
     completer should be added.  It can be one of the following values:
       * "start" indicates that the completer should be added to the start of
                 the list of completers (it should be run before all others)
       * "end" indicates that the completer should be added to the end of the
               list of completers (it should be run after all others)
       * ">KEY", where KEY is a pre-existing name, indicates that this should
                 be added after the completer named KEY
       * "<KEY", where KEY is a pre-existing name, indicates that this should
                 be added before the completer named KEY

     If POS is not provided, the default value is "start"
"""

#
# commands
#
# amalgamated os
# amalgamated builtins
xt = _LazyModule.load('xonsh', 'xonsh.tools', 'xt')
# amalgamated xonsh.platform
# amalgamated xonsh.completers.tools
SKIP_TOKENS = {'sudo', 'time', 'timeit', 'which', 'showcmd', 'man'}


def complete_command(cmd, line, start, end, ctx):
    """
    Returns a list of valid commands starting with the first argument
    """
    space = ' '
    out = {s + space
           for s in builtins.__xonsh_commands_cache__
           if get_filter_function()(s, cmd)}
    if xp.ON_WINDOWS:
        out |= {i for i in xt.executables_in('.')
                if i.startswith(cmd)}
    base = os.path.basename(cmd)
    if os.path.isdir(base):
        out |= {os.path.join(base, i)
                for i in xt.executables_in(base)
                if i.startswith(cmd)}
    return out


def complete_skipper(cmd, line, start, end, ctx):
    """
    Skip over several tokens (e.g., sudo) and complete based on the rest of the
    line.
    """
    res = line.split(' ', 1)
    if len(res) == 2:
        first, rest = res
    else:
        first = res[0]
        rest = ''
    if first in SKIP_TOKENS:
        comp = builtins.__xonsh_shell__.shell.completer
        res = rest.split(' ', 1)
        if len(res) == 1:
            comp_func = complete_command
        else:
            comp_func = comp.complete
        return comp_func(cmd,
                         rest,
                         start - len(first) - 1,
                         end - len(first) - 1,
                         ctx)
    else:
        return set()

#
# man
#
# amalgamated os
# amalgamated re
# amalgamated pickle
# amalgamated builtins
# amalgamated subprocess
# amalgamated xonsh.lazyasd
# amalgamated xonsh.completers.tools
OPTIONS = None
OPTIONS_PATH = None


@xl.lazyobject
def SCRAPE_RE():
    return re.compile(r'^(?:\s*(?:-\w|--[a-z0-9-]+)[\s,])+', re.M)


@xl.lazyobject
def INNER_OPTIONS_RE():
    return re.compile(r'-\w|--[a-z0-9-]+')


def complete_from_man(prefix, line, start, end, ctx):
    """
    Completes an option name, based on the contents of the associated man
    page.
    """
    global OPTIONS, OPTIONS_PATH
    if OPTIONS is None:
        datadir = builtins.__xonsh_env__['XONSH_DATA_DIR']
        OPTIONS_PATH = os.path.join(datadir, 'man_completions_cache')
        try:
            with open(OPTIONS_PATH, 'rb') as f:
                OPTIONS = pickle.load(f)
        except Exception:
            OPTIONS = {}
    if not prefix.startswith('-'):
        return set()
    cmd = line.split()[0]
    if cmd not in OPTIONS:
        try:
            manpage = subprocess.Popen(
                ["man", cmd], stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL)
            # This is a trick to get rid of reverse line feeds
            text = subprocess.check_output(
                ["col", "-b"], stdin=manpage.stdout)
            text = text.decode('utf-8')
            scraped_text = ' '.join(SCRAPE_RE.findall(text))
            matches = INNER_OPTIONS_RE.findall(scraped_text)
            OPTIONS[cmd] = matches
            with open(OPTIONS_PATH, 'wb') as f:
                pickle.dump(OPTIONS, f)
        except Exception:
            return set()
    return {s for s in OPTIONS[cmd]
            if get_filter_function()(s, prefix)}

#
# path
#
# amalgamated os
ast = _LazyModule.load('ast', 'ast')
# amalgamated builtins
# amalgamated xonsh.tools
# amalgamated xonsh.platform
# amalgamated xonsh.lazyasd
# amalgamated xonsh.completers.tools
@xl.lazyobject
def CHARACTERS_NEED_QUOTES():
    cnq = ' `\t\r\n${}*()"\',?&'
    if xp.ON_WINDOWS:
        cnq += '%'
    return cnq


def _path_from_partial_string(inp, pos=None):
    if pos is None:
        pos = len(inp)
    partial = inp[:pos]
    startix, endix, quote = xt.check_for_partial_string(partial)
    _post = ""
    if startix is None:
        return None
    elif endix is None:
        string = partial[startix:]
    else:
        if endix != pos:
            _test = partial[endix:pos]
            if not any(i == ' ' for i in _test):
                _post = _test
            else:
                return None
        string = partial[startix:endix]
    end = xt.RE_STRING_START.sub('', quote)
    _string = string
    if not _string.endswith(end):
        _string = _string + end
    try:
        val = ast.literal_eval(_string)
    except SyntaxError:
        return None
    if isinstance(val, bytes):
        env = builtins.__xonsh_env__
        val = val.decode(encoding=env.get('XONSH_ENCODING'),
                         errors=env.get('XONSH_ENCODING_ERRORS'))
    return string + _post, val + _post, quote, end


def _normpath(p):
    """
    Wraps os.normpath() to avoid removing './' at the beginning
    and '/' at the end. On windows it does the same with backslashes
    """
    initial_dotslash = p.startswith(os.curdir + os.sep)
    initial_dotslash |= (xp.ON_WINDOWS and p.startswith(os.curdir + os.altsep))
    p = p.rstrip()
    trailing_slash = p.endswith(os.sep)
    trailing_slash |= (xp.ON_WINDOWS and p.endswith(os.altsep))
    p = os.path.normpath(p)
    if initial_dotslash and p != '.':
        p = os.path.join(os.curdir, p)
    if trailing_slash:
        p = os.path.join(p, '')
    if xp.ON_WINDOWS and builtins.__xonsh_env__.get('FORCE_POSIX_PATHS'):
        p = p.replace(os.sep, os.altsep)
    return p


def _startswithlow(x, start, startlow=None):
    if startlow is None:
        startlow = start.lower()
    return x.startswith(start) or x.lower().startswith(startlow)


def _startswithnorm(x, start, startlow=None):
    return x.startswith(start)


def _env(prefix):
    if prefix.startswith('$'):
        key = prefix[1:]
        return {'$' + k
                for k in builtins.__xonsh_env__
                if get_filter_function()(k, key)}
    return ()


def _dots(prefix):
    slash = xt.get_sep()
    if slash == '\\':
        slash = ''
    if prefix in {'', '.'}:
        return ('.'+slash, '..'+slash)
    elif prefix == '..':
        return ('..'+slash,)
    else:
        return ()


def _add_cdpaths(paths, prefix):
    """Completes current prefix using CDPATH"""
    env = builtins.__xonsh_env__
    csc = env.get('CASE_SENSITIVE_COMPLETIONS')
    glob_sorted = env.get('GLOB_SORTED')
    for cdp in env.get('CDPATH'):
        test_glob = os.path.join(cdp, prefix) + '*'
        for s in xt.iglobpath(test_glob, ignore_case=(not csc),
                              sort_result=glob_sorted):
            if os.path.isdir(s):
                paths.add(os.path.basename(s))


def _quote_to_use(x):
    single = "'"
    double = '"'
    if single in x and double not in x:
        return double
    else:
        return single


def _quote_paths(paths, start, end):
    expand_path = builtins.__xonsh_expand_path__
    out = set()
    space = ' '
    backslash = '\\'
    double_backslash = '\\\\'
    slash = xt.get_sep()
    orig_start = start
    orig_end = end
    for s in paths:
        start = orig_start
        end = orig_end
        if (start == '' and
                (any(i in s for i in CHARACTERS_NEED_QUOTES) or
                 (backslash in s and slash != backslash))):
            start = end = _quote_to_use(s)
        if os.path.isdir(expand_path(s)):
            _tail = slash
        elif end == '':
            _tail = space
        else:
            _tail = ''
        if start != '' and 'r' not in start and backslash in s:
            start = 'r%s' % start
        s = s + _tail
        if end != '':
            if "r" not in start.lower():
                s = s.replace(backslash, double_backslash)
            if s.endswith(backslash) and not s.endswith(double_backslash):
                s += backslash
        if end in s:
            s = s.replace(end, ''.join('\\%s' % i for i in end))
        out.add(start + s + end)
    return out


def _joinpath(path):
    # convert our tuple representation back into a string representing a path
    if path is None:
        return ''
    elif len(path) == 0:
        return ''
    elif path == ('',):
        return xt.get_sep()
    elif path[0] == '':
        return xt.get_sep() + _normpath(os.path.join(*path))
    else:
        return _normpath(os.path.join(*path))


def _splitpath(path):
    # convert a path into an intermediate tuple representation
    # if this tuple starts with '', it means that the path was an absolute path
    path = _normpath(path)
    if path.startswith(xt.get_sep()):
        pre = ('', )
    else:
        pre = ()
    return pre + _splitpath_helper(path, ())


def _splitpath_helper(path, sofar=()):
    folder, path = os.path.split(path)
    if path == "":
        return sofar[::-1]
    elif folder == "":
        return (sofar + (path, ))[::-1]
    else:
        return _splitpath_helper(folder, sofar + (path, ))


def subsequence_match(ref, typed, csc):
    """
    Detects whether typed is a subsequence of ref.

    Returns ``True`` if the characters in ``typed`` appear (in order) in
    ``ref``, regardless of exactly where in ``ref`` they occur.  If ``csc`` is
    ``False``, ignore the case of ``ref`` and ``typed``.

    Used in "subsequence" path completion (e.g., ``~/u/ro`` expands to
    ``~/lou/carcohl``)
    """
    if csc:
        return _subsequence_match_iter(ref, typed)
    else:
        return _subsequence_match_iter(ref.lower(), typed.lower())


def _subsequence_match_iter(ref, typed):
    if len(typed) == 0:
        return True
    elif len(ref) == 0:
        return False
    elif ref[0] == typed[0]:
        return _subsequence_match_iter(ref[1:], typed[1:])
    else:
        return _subsequence_match_iter(ref[1:], typed)


def _expand_one(sofar, nextone, csc):
    out = set()
    glob_sorted = builtins.__xonsh_env__.get('GLOB_SORTED')
    for i in sofar:
        _glob = os.path.join(_joinpath(i), '*') if i is not None else '*'
        for j in xt.iglobpath(_glob, sort_result=glob_sorted):
            j = os.path.basename(j)
            if subsequence_match(j, nextone, csc):
                out.add((i or ()) + (j, ))
    return out


def complete_path(prefix, line, start, end, ctx, cdpath=True, filtfunc=None):
    """Completes based on a path name."""
    # string stuff for automatic quoting
    path_str_start = ''
    path_str_end = ''
    p = _path_from_partial_string(line, end)
    lprefix = len(prefix)
    if p is not None:
        lprefix = len(p[0])
        prefix = p[1]
        path_str_start = p[2]
        path_str_end = p[3]
    tilde = '~'
    paths = set()
    env = builtins.__xonsh_env__
    csc = env.get('CASE_SENSITIVE_COMPLETIONS')
    glob_sorted = env.get('GLOB_SORTED')
    for s in xt.iglobpath(prefix + '*', ignore_case=(not csc),
                          sort_result=glob_sorted):
        paths.add(s)
    if len(paths) == 0 and env.get('SUBSEQUENCE_PATH_COMPLETION'):
        # this block implements 'subsequence' matching, similar to fish and zsh.
        # matches are based on subsequences, not substrings.
        # e.g., ~/u/ro completes to ~/lou/carcolh
        # see above functions for details.
        p = _splitpath(os.path.expanduser(prefix))
        if len(p) != 0:
            if p[0] == '':
                basedir = ('', )
                p = p[1:]
            else:
                basedir = None
            matches_so_far = {basedir}
            for i in p:
                matches_so_far = _expand_one(matches_so_far, i, csc)
            paths |= {_joinpath(i) for i in matches_so_far}
    if len(paths) == 0 and env.get('FUZZY_PATH_COMPLETION'):
        threshold = env.get('SUGGEST_THRESHOLD')
        for s in xt.iglobpath(os.path.dirname(prefix) + '*',
                              ignore_case=(not csc),
                              sort_result=glob_sorted):
            if xt.levenshtein(prefix, s, threshold) < threshold:
                paths.add(s)
    if tilde in prefix:
        home = os.path.expanduser(tilde)
        paths = {s.replace(home, tilde) for s in paths}
    if cdpath:
        _add_cdpaths(paths, prefix)
    paths = set(filter(filtfunc, paths))
    paths = _quote_paths({_normpath(s) for s in paths},
                         path_str_start,
                         path_str_end)
    paths.update(filter(filtfunc, _dots(prefix)))
    paths.update(filter(filtfunc, _env(prefix)))
    return paths, lprefix


def complete_dir(prefix, line, start, end, ctx, cdpath=False):
    return complete_path(prefix, line, start, end, cdpath,
                         filtfunc=os.path.isdir)

#
# python
#
"""Completers for Python code"""
# amalgamated re
sys = _LazyModule.load('sys', 'sys')
inspect = _LazyModule.load('inspect', 'inspect')
# amalgamated builtins
importlib = _LazyModule.load('importlib', 'importlib')
abc = _LazyModule.load('collections', 'collections.abc', 'abc')
# amalgamated xonsh.tools
# amalgamated xonsh.lazyasd
# amalgamated xonsh.completers.tools
@xl.lazyobject
def RE_ATTR():
    return re.compile(r'([^\s\(\)]+(\.[^\s\(\)]+)*)\.(\w*)$')


@xl.lazyobject
def XONSH_TOKENS():
    return {
        'and ', 'as ', 'assert ', 'break', 'class ', 'continue', 'def ', 'del ',
        'elif ', 'else', 'except ', 'finally:', 'for ', 'from ', 'global ',
        'import ', 'if ', 'in ', 'is ', 'lambda ', 'nonlocal ', 'not ', 'or ',
        'pass', 'raise ', 'return ', 'try:', 'while ', 'with ', 'yield ', '+',
        '-', '/', '//', '%', '**', '|', '&', '~', '^', '>>', '<<', '<', '<=',
        '>', '>=', '==', '!=', '->', '=', '+=', '-=', '*=', '/=', '%=', '**=',
        '>>=', '<<=', '&=', '^=', '|=', '//=', ',', ';', ':', '?', '??', '$(',
        '${', '$[', '..', '...', '![', '!(', '@(', '@$(', '@'
        }


def complete_python(prefix, line, start, end, ctx):
    """
    Completes based on the contents of the current Python environment,
    the Python built-ins, and xonsh operators.
    """
    if line != '':
        first = line.split()[0]
        if first in builtins.__xonsh_commands_cache__ and first not in ctx:
            return set()
    filt = get_filter_function()
    rtn = {s for s in XONSH_TOKENS if filt(s, prefix)}
    if ctx is not None:
        if '.' in prefix:
            rtn |= attr_complete(prefix, ctx, filt)
        rtn |= {s for s in ctx if filt(s, prefix)}
    rtn |= {s for s in dir(builtins) if filt(s, prefix)}
    return rtn


def complete_python_mode(prefix, line, start, end, ctx):
    """
    Python-mode completions for @( and ${
    """
    if not (prefix.startswith('@(') or prefix.startswith('${')):
        return set()
    prefix_start = prefix[:2]
    python_matches = complete_python(prefix[2:], line, start+2, end, ctx)
    return set(prefix_start + i for i in python_matches)


def attr_complete(prefix, ctx, filter_func):
    """Complete attributes of an object."""
    attrs = set()
    m = RE_ATTR.match(prefix)
    if m is None:
        return attrs
    expr, attr = m.group(1, 3)
    expr = xt.subexpr_from_unbalanced(expr, '(', ')')
    expr = xt.subexpr_from_unbalanced(expr, '[', ']')
    expr = xt.subexpr_from_unbalanced(expr, '{', '}')
    _ctx = None
    xonsh_safe_eval = builtins.__xonsh_execer__.eval
    try:
        val = xonsh_safe_eval(expr, ctx, transform=False)
        _ctx = ctx
    except:  # pylint:disable=bare-except
        try:
            val = xonsh_safe_eval(expr, builtins.__dict__, transform=False)
            _ctx = builtins.__dict__
        except:  # pylint:disable=bare-except
            return attrs  # anything could have gone wrong!
    if len(attr) == 0:
        opts = [o for o in dir(val) if not o.startswith('_')]
    else:
        opts = [o for o in dir(val) if filter_func(o, attr)]
    prelen = len(prefix)
    for opt in opts:
        # check whether these options actually work (e.g., disallow 7.imag)
        try:
            _val = '{0}.{1}'.format(expr, opt)
            xonsh_safe_eval(_val, _ctx, transform=False)
        except:  # pylint:disable=bare-except
            continue
        a = getattr(val, opt)
        if callable(a):
            rpl = opt + '('
        elif isinstance(a, abc.Iterable):
            rpl = opt + '['
        else:
            rpl = opt
        # note that prefix[:prelen-len(attr)] != prefix[:-len(attr)]
        # when len(attr) == 0.
        comp = prefix[:prelen - len(attr)] + rpl
        attrs.add(comp)
    return attrs


def complete_import(prefix, line, start, end, ctx):
    """
    Completes module names and contents for "import ..." and "from ... import
    ..."
    """
    ltoks = line.split()
    if len(ltoks) == 2 and ltoks[0] == 'from':
        # completing module to import
        return {'{} '.format(i) for i in complete_module(prefix)}
    if ltoks[0] == 'import' and start == len('import '):
        # completing module to import
        return complete_module(prefix)
    if len(ltoks) > 2 and ltoks[0] == 'from' and ltoks[2] == 'import':
        # complete thing inside a module
        try:
            mod = importlib.import_module(ltoks[1])
        except ImportError:
            return set()
        out = {i[0]
               for i in inspect.getmembers(mod)
               if i[0].startswith(prefix)}
        return out
    return set()


def complete_module(prefix):
    return {s for s in sys.modules if get_filter_function()(s, prefix)}

#
# base
#
"""Base completer for xonsh."""
# amalgamated xonsh.completers.path
# amalgamated xonsh.completers.python
# amalgamated xonsh.completers.commands
def complete_base(prefix, line, start, end, ctx):
    """If the line is empty, complete based on valid commands, python names,
    and paths.  If we are completing the first argument, complete based on
    valid commands and python names.
    """
    if line.strip() == '':
        out = (complete_python(prefix, line, start, end, ctx) |
               complete_command(prefix, line, start, end, ctx))
        paths = complete_path(prefix, line, start, end, ctx, False)
        return (out | paths[0]), paths[1]
    elif prefix == line:
        return (complete_python(prefix, line, start, end, ctx) |
                complete_command(prefix, line, start, end, ctx))
    return set()

#
# dirs
#
# amalgamated xonsh.completers.man
# amalgamated xonsh.completers.path
def complete_cd(prefix, line, start, end, ctx):
    """
    Completion for "cd", includes only valid directory names.
    """
    if start != 0 and line.split(' ')[0] == 'cd':
        return complete_dir(prefix, line, start, end, ctx, True)
    return set()


def complete_rmdir(prefix, line, start, end, ctx):
    """
    Completion for "rmdir", includes only valid directory names.
    """
    if start != 0 and line.split(' ')[0] == 'rmdir':
        opts = {i for i in complete_from_man('-', 'rmdir -', 6, 7, ctx)
                if i.startswith(prefix)}
        comps, lp = complete_dir(prefix, line, start, end, ctx, True)
        return comps | opts, lp
    return set()

#
# init
#
"""Constructor for xonsh completer objects."""
# amalgamated collections
# amalgamated xonsh.completers.pip
# amalgamated xonsh.completers.man
# amalgamated xonsh.completers.bash
# amalgamated xonsh.completers.base
# amalgamated xonsh.completers.path
# amalgamated xonsh.completers.dirs
# amalgamated xonsh.completers.python
# amalgamated xonsh.completers.commands
# amalgamated xonsh.completers.completer
def default_completers():
    """Creates a copy of the default completers."""
    return collections.OrderedDict([
        ('python_mode', complete_python_mode),
        ('base', complete_base),
        ('completer', complete_completer),
        ('skip', complete_skipper),
        ('pip', complete_pip),
        ('cd', complete_cd),
        ('rmdir', complete_rmdir),
        ('bash', complete_from_bash),
        ('man', complete_from_man),
        ('import', complete_import),
        ('python', complete_python),
        ('path', complete_path),
        ])

