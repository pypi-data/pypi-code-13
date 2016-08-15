# -*- coding: utf-8 -*-
"""The FileSysObjects package provides operations on paths, path parts and side branches. 

For extended additional information refer to the manuals, offline, or online at
"https://pythonhosted.org/pyfilesysobjects/".
Create manuals from sources by: "python setup.py build_sphinx" 
and "python setup.py build_epydoc"

The current version calls 'os.path.normpath' by default - when 'raw' is 
not selected. This is consistent for all path related parameters including
search paths: start, top, plist, spath, etc.. Thus generally clears double 
slashes, but also replaces symbolic links, so later literal post processing
e.g. for match based processing should be normalized too.
        
There is one exception due to for leading '//' and '\\\\', see option 'ias'
and  IEEE Std 1003.1(TM), UNC, and SMB/CIFS for Pathname Resolution.
Current supported URIs for filenames are: 'file://', 'smb://', and 
'cifs://'.

The following options are generic and common to multiple interfaces:

    **spath**: An existing path to be added to an entry 
        from 'plist'. The following cases are supported,
        for further specifics refer to the interfaces.

        0. Independent path entry:
           spath is absolute, just added.
           
        1. Subpath of current directory
           spath is relative and present in
           current working directory, added
           py prefixing 'pwd'.
            
        2. Arbitrary side-branch of a provided path 
           spath is relative, searched in plist
           for an insertion hook, added when 
           found as absolute.
           
        3. Pattern matching - see manual 'Semi-Literals':
           regexpr: Regular expressions are applicable for 
               match on 'plist' only. Thus the part to be 
               matched on the filesystem is required to be a 
               literal. 
           glob: Glob expressions are applicable on the filesystem
               itself only, thus the part to be matched on the
               'plist' is required to be a literal.

        4. Is absolute path:
            Is checked to be a subpath of at least one of 'plist',
            than applied. 

    **start**: Start directory or file, when a file is provided the 
        directory portion is used as the starting pointer.

        Each part is compared separately, but as a whole string.
    
    **top**: The topmost path within a directory tree as an end point 
        for a search operation. This is defined by the end of 
        a directory path name string. E.g. the the bottom-up search 
        beginning at the start directory::

           start=/a/b/c/d/e/f/g 
    
        is terminated by""::

           top=d
           
        at::

           /a/b/c/d
        
        This is used as a match string for processing literally 
        on the parts of the provided start directory. The match 
        is checked after application of
        'os.path.normpath'. Providing absolute paths still match,
        because of the string, but eventually match multiple times
        when equal subpaths exist and the match order is changed 
        to bottom-up search. 
        
        The containment of 'top' within the absolute 'start' path 
        is verified. 

        Each part is compared separately, but as a whole string.
        
    **plist**: List of strings to be searched. By default first match
        is used. Each is splitted into it's components and matched
        separately.
        
        default := sys.path

    **matchidx=#idx**: Matches on the provided index count only
        ::
        
           #idx==2 - ignores 0,1 and >2, matches idx==2

    **matchcnt=#num**: The maximal number of matches returned when
        multiple occur::
        
           #num==0 - all
           #num>0  - number of matches returned

    **matchlvl=#num**: Increment of match for top node when multiple 
        are in the path. The counter starts at top, so #num(1) will
        match M(1) in::
        
            /a/b/M/c/M/d/M/w/e/M/bottom
                 0   1   2     3
                 |   *
                 |
                 `-default

    **matchlvlupward=#num**: Increment of match for top node when multiple
        are in the path. The counter starts from the bottom, so #num(2)
        will match M(2) in::
        
            /a/b/M/c/M/d/M/w/e/M/bottom
                 3   2   1     0
                     *

    **raw**: Suppress normalization by call of 'os.path.normpath'. The 
        caller has than to take care for appropriate measures for 
        a feasible match. 

    **ias**: Treats for local file names any number of 
        subsequent '/' only as one, also leading pattern '//[^/]+'. 
        URI prefixes are treated correctly.

        See also "IEEE Std 1003.1(TM), 2013 Edition; Chap. 4.12".

"""
from __future__ import absolute_import
from __builtin__ import True

__author__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2010-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.1.8'
__uuid__ = '9de52399-7752-4633-9fdc-66c87a9200b8'

__docformat__ = "restructuredtext en"

import os, sys
version = '{0}.{1}'.format(*sys.version_info[:2])
if version < '2.7':  # pragma: no cover
    raise Exception("Requires Python-2.7.* or higher")

from types import NoneType
import re, glob
import platform

from pysourceinfo.PySourceInfo import getCallerModuleFilePathName,getCallerModulePathName, getPythonPathRel,getCallerPathName

class FileSysObjectsException(Exception):
    pass

#
# for test and development
_mydebug = False
# _mydebug = True

#*
# *** static compiled strings ***
#*

# FIXME: if os....
_CPREP = re.compile(ur"^[/\\\\]*(.*)[/\\\\]*$")  # prepares split
ISAPPPATHc = re.compile(ur'[/\\\\]{2}([^/\\\\]+)[/\\\\]+(.*)')  # splits app part from path - IEEE-1003.1, CIFS/SMB/UNC(simple)
# _DIRSPLT = re.compile(ur"""^([a-z][:])*(.*)$""")


# types 
PTYPES     = ( 'SHARE', 'SMB', 'CIFS',  'SHARE', 'LDSYS',  'LFSYS', 'IAS',)

# type of regexpr groups
PGTYPE     = ( 'SHARE', 'SMB', 'CIFS',  'SHARE', 'LDSYS', 'LFSYS', 'LDSYS', 'LDSYS', 'IAS', 'LFSYS',)


#
# *** checks type ***
#
_COMPT = re.compile(ur"""
 ((file:///[/\\\\]{2})()([^/\\\\]{0,1}.*))            # file and share
 |((smb://)()(.*))                                    # smb
 |((cifs://)()(.*))                                   # cifs
 |(([/\\\\])()([/\\\\][^/\\\\]{0,1}.*))               # share
 |((file://)([a-zA-Z][:])([/\\\\]*?[/\\\\]{0,1}.*))   # file and drive, could not be a share, thus nothing to ignore
 |((file://)[/\\\\]*?()([/\\\\]{0,1}.*))              # local file, could not be a share, thus nothing to ignore 
 |(()([a-zA-Z][:])[/\\\\]*?([/\\\\].*))               # drive-path win, could not be a share, thus nothing to ignore
 |(()([a-zA-Z][:])[/\\\\]*?(.*))                      # drive-path win, could not be a share, thus nothing to ignore
 |((ias://)()(.*))                                    # ias - internal type for test 'IgnoreAppSeperator'
 |(()()(.*))                                          # generic
 """,
 re.X
)
_COMPTg    = [ 1,       5,     9,       13,      17,      21,      25,      29,      33,     37,      ]
#PGTYPE    = ( 'SHARE', 'SMB', 'CIFS',  'SHARE', 'LDSYS', 'LFSYS', 'LDSYS', 'LDSYS', 'IAS',  'LFSYS', )

#
# *** splits into type specifc components ***
#
# extended pathname with basic network prefix
_COMPX = re.compile(ur"""
 ((file:///[/\\\\]{2})(.{0,1}[^/\\\\]+)[/\\\\]+([^/\\\\]+)[/\\\\]*(.*))#  2: ('file:///' +2SEP) +(SPECIALNODE) +varSEP    +(share-name) +(path)
 |((smb://)([^/]{01}[^/\\\\]*)[/\\\\]+([^/\\\\]+)[/\\\\]*(.*))         #  7: ('smb://'  )          +(SPECIALNODE) +varSEP    +(share-name) +(path)
 |((cifs://)([^/]{01}[^/\\\\]*)[/\\\\]+([^/\\\\]+)[/\\\\]*(.*))        # 12: ('cifs://'  )           +(SPECIALNODE) +varSEP    +(share-name) +(path)
 |(([/\\\\]{2})([^/\\\\]+)[/\\\\]*([^/\\\\]+)[/\\\\]+(.*))             # 17: (2SEP    )          +(SPECIALNODE) +varSEP    +(share-name) +(path) # in general a share present - on POSIX too???
 |((file://)()([a-zA-Z]:)[/\\\\]*?([/\\\\]{0,1}.*))                    # 22: ('file://'     )         +()                            +varSEP    +(drive)             +(path)
 |((file://)()()(.*))                                                  # 27: ('file://'     )         +()                            +varSEP    +()                     +(path)
 |(()()([a-zA-Z]:)[/\\\\]*?([/\\\\].*))                                # 32: ()                       +()                            +()              +(drive)             +(path)
 |(()()([a-zA-Z]:)[/\\\\]*?(.*))                                       # 37: ()                       +()                            +()              +(drive)             +(path)
 |((ias://)()()(.*))                                                   # 27: ('ias://'     )        +()                            +varSEP    +()                      +(path-for-test)
 |(()()()(.*))                                                         # 42: ()                        +()                            +nSEP       +()                     +(path)
 """,
 re.X
)
_COMPXg    = [ 2,       7,     12,      17,      22,      27,      32,      37,      42,     47,      ]
#PGTYPE    = ( 'SHARE', 'SMB', 'CIFS',  'SHARE', 'LDSYS', 'LFSYS', 'LDSYS', 'LDSYS', 'IAS',  'LFSYS', )


def addPathToSearchPath(spath, plist=None, **kargs):
    """Adds a path to 'plist'. 

    In case of relative paths searches in provided 
    'plist', or 'kargs[searchplist]'a hook, when found 
    verifies the existence within file system, in case 
    of success adds the completed path to 'plist' the list.
    
    In case of 'glob' adds all entries.

    Args:
        spath: A path to be added to 'plist'.
            See common options for details.
            Valid scope types:

                * literal : X
                * re      : -
                * blob    : -

            default := caller-file-position.

        plist: List to for the storage, and by default
            search list too.
            See common options for details.
        
            default := sys.path

        **kargs:
            append: Append, this is equal to
                pos=len(plist).
                
            checkreal: Checks redundancy py resolving realpath,
                else literlaly.

            exist: Checks whether exists, else nothing is done. 

            pos=#pos: A specific position for insertion
                within range(0,len(plist)).
            
            prepend: Prepend, this is equal to
                pos=0.
                
            redundant: Add relative, allow redundant when
                same is already present.

            relative=<base>: Add relative subpath to 
                provided base.

            searchplist: Alternative list to search for checks.

    Returns:
        When successful returns insertion position, else a 'value<0'.
        The insertion position in case of multiple items is the position 
        of the last.

    Raises:
        passed through exceptions:
    """
    if type(plist) == NoneType:
        plist = sys.path

    _splist = kargs.get('searchplist', plist)

    pos = 0
    relative = None
    _exist = False
    _red = False
    _chkr = False
    for k, v in kargs.items():
        if k == 'prepend':
            pos = 0
        elif k == 'append':
            pos = -1
        elif k == 'pos':
            if not type(v) is int:
                raise FileSysObjectsException("Digits required for 'pos'*" + str(pos) + ")")
            pos = v
        elif k == 'relative':
            relative = v.split(os.pathsep)
        elif k == 'exists':
            _exist = v
        elif k == 'redundant':
            _red = v
        elif k == 'checkreal':
            _chkr = v

    def _add(s):
        if relative:
            s = getPythonPathRel(s, relative)
        if not _red:
            if _chkr:
                for sx in map(lambda x:os.path.realpath(x), plist):
                    if os.path.realpath(s) == sx:
                        return
            else:
                if s in plist:
                    return

        if pos == -1:
            plist.append(s)
            return len(plist) - 1
        else:
            plist.insert(pos, s)
            return pos

    # normalize
    _start_elems = splitAppPrefix(spath,**kargs)
    spath = getAppPrefixLocalPath(_start_elems)

    if _exist:
        if os.path.isabs(spath) and os.path.exists(spath):
            return _add(spath)
        elif os.path.exists(os.path.curdir + os.sep + spath):
            return _add(os.path.normpath(os.path.curdir + os.sep + spath))
        else: 
            for s in _splist[:]:
                if os.path.exists(s + os.sep + spath):
                    pos = _add(s + os.sep + spath)
    else:
        if os.path.isabs(spath):
            return _add(spath)
        elif os.path.exists(os.path.curdir + os.sep + spath):
            return _add(os.path.normpath(os.path.curdir + os.sep + spath))
        else: 
            for s in _splist[:]:
                if os.path.exists(s + os.sep + spath):
                    pos = _add(s + os.sep + spath)
    return pos

def clearPath(plist=None, **kargs):
    """Clears, splits and joins a list of path variables by various criteria.
    
    Args:
        plist: List of paths to be cleared.
            See common options for details.
            
            default := sys.path

        **kargs:
            abs: Converts all entries into absolute pathnames.
            
            existent: Removes all existing items. For test 
                and verification.

            ias: Treats for local file names any 
                number of subsequent '/' only as one.
                
                See common options for details.

            non-existent: Removes all items which do not exist.
            
            non-redundant: Removes all items which are not redundant.
                Results e.g. in multiple incarnations of the same 
                file/path type.

            normpath: Calls 'os.path.normpath' on each result.

            redundant: Clears all items from redundancies.

            rel:  Converts all entries into relative pathnames.

            reverse: This reverses the resulting search order 
                 from bottom-up to top-down. Takes effect on
                 'redundant' only.

            shrink: Drops resulting empty items. 

            split: Forces split of multiple paths items within
                one item into seperate item entries.

                default := noSplit
            withinItemOnly: Performs any action for each 
                item of 'plist' only.
            

    Returns:
        When successful returns 'True', else returns either 'False', 
        or raises an exception.

    Raises:
        passed through exceptions:
    """
    if plist == None:
        plist = sys.path
    
    _abs = False
    _existent = False
    _ias = False
    _links = False
    _ne = False
    _nr = False
    _normpath = False
    _redundant = False
    _rel = False
    _reverse = False
    _wio = False
    _shrink = False
    _split = False

    for k, v in kargs.items():
        if k == 'abs':
            _abs = v
        elif k == 'existent':
            _existent = v
        elif k == 'ias':
            _ias = v
        elif k == 'links':
            _links = v
        elif k == 'non-existent':
            _ne = v
        elif k == 'non-redundant':
            _nr = v
        elif k == 'normpath':
            _normpath = v
        elif k == 'redundant':
            _redundant = v
        elif k == 'rel':
            _rel = v
        elif k == 'reverse':
            _reverse = v
        elif k == 'withinItemOnly':
            _wio = v
        elif k == 'shrink':
            _shrink = v
        elif k == 'split':
            _split = v

    def clearIt(px, ref=None):
        """the actual workhorse
        
        px:  patch to process
        ref: reference path
        """
        if _abs:
            px = os.path.abspath(px)
        if _existent and os.path.exists(px):
            return
        if _ne and not os.path.exists(px):
            return
        if _normpath:
            px = os.path.normpath(px)
        if _ias and px[:2] == os.sep + os.sep:
            px = px[1:]
        if _rel:
            px = getPythonPathRel(px, plist)        
        return px

    def clrred(x):
        """clear redundancies"""
        if x in clearPath._clearlst:
            return
        clearPath._clearlst.append(x)
        return x

    #
    # --------------------------------------------
    #
    if not _wio:
        clearPath._clearlst = []
    pn = plist[:] # input list
    
    if _reverse: #reveser input list 
        pn.reverse()
    for p in range(len(plist)): plist.pop() # clear source for new items - in place of caller

    #
    # split items into subitems as seeprate new items
    if _split:
        _pn = []
        for p in pn:
            if p:
                for px in p.split(os.pathsep):
                    _pn.append(px)
        pn = _pn

    #
    # work out items
    for p in pn:  # each item

        # within item only
        if _wio:
            clearPath._clearlst = []
        pn = ''
        
        # reverse order
        if _reverse:
            plx = p.split(os.pathsep)
            plx.reverse()
        else:
            plx = p.split(os.pathsep)
        
        #clear redundancies
        for p1 in plx:
            if _redundant: px = clrred(clearIt(p1))
            else: px = clearIt(p1)
            if _shrink:
                if px: pn += os.pathsep + px
            else: 
                if px: pn += os.pathsep + px
                else: pn += os.pathsep

        if pn: pn = pn[1:]
        if _reverse and pn:
            plx = pn.split(os.pathsep)
            plx.reverse()
            pn = os.pathsep.join(plx)
        
        # schrink
        if _shrink:  
            if pn: plist.append(pn)
        else: plist.append(pn)

    if _reverse: 
        plist.reverse()

def delPathFromSearchPath(dellist, plist=None, **kargs):
    """Deletes a list of paths from 'plist'. 

    Args:
        dellist: A list of paths to be deleted 
            from 'plist'. Valid scope types:

                * literal : X
                * re      : X
                * glob    : X

            see kargs[regexpr|glob].

            default := None

        plist: List of search paths.
        
            default := sys.path

        **kargs:
            The following keys are additional before 
            comparison, on 'dellist' only when no
            match pattern is provided:

                case: Calls on both: os.path.normcase
    
                esc: Calls on both: escapeFilePath/unescapeFilePath
                
                exist: Calls on both: os.path.exists
                
                noexist: Calls on both: not os.path.exists
            
                normX: Calls on both: normpathX

                norm: Calls on both: os.path.normpath

                real: Calls on both: os.path.realpath
                
            regexpr|glob: Input is a list of

                regexpr: regular expressions,
                    just processed by 
                        're.match(dl,pl)'
 
                glob: process glob, and check 
                    containment in set

    Returns:
        When successful returns True, else False.

    Raises:
        passed through exceptions
        
    """
    if type(plist) == NoneType:
        plist = sys.path
    if not dellist:
        return True
    _exists = False
    _rg = False
    _raw = kargs.get('raw', False)
    _real = kargs.get('real', False)
    _norm = kargs.get('norm', False)
    _case = kargs.get('case', False)

    for k, v in kargs.items():  # @UnusedVariable
        if k == 'exist':
            _exist = True
            _exists = True
        elif k == 'noexist':
            _exist = False
            _exists = True

        elif k == 'regexpr':
            _reg = True
            _glob = False
            __rg = True
        elif k == 'glob':
            _reg = False
            _glob = True
            __rg = True

    # seems to be sure
    if type(dellist) == str:
        dellist = [dellist]

    for dl in dellist:
        for pl in reversed(plist):
            if not _raw:
                if dl and len(dl) > 6 and dl[0:7] == 'file://':
                    dl = os.sep + dl[7:].lstrip(os.sep) 
                if pl and len(pl) > 6 and pl[0:7] == 'file://':
                    pl = os.sep + pl[7:].lstrip(os.sep) 
            if _real:
                if not _rg: 
                    dl = os.path.realpath(dl)
                pl = os.path.realpath(pl)
            if _norm:
                if not _rg: 
                    dl = os.path.normpath(dl)
                pl = os.path.normpath(pl)
            if _case:
                if not _rg: 
                    dl = os.path.normcase(dl)
                pl = os.path.normcase(pl)

            if _exists:
                if _exist:
                    if not _rg: 
                        if not os.path.exists(pl) or not os.path.exists(dl): 
                            continue
                    elif os.path.exists(pl): 
                        continue

            if _rg:
                if _reg:
                    if re.match(dl, pl):
                        plist.pop(plist.index(pl))
                elif _glob:
                    if pl in glob.glob(dl):
                        plist.pop(plist.index(pl))
            else:
                if dl == pl:
                    plist.pop(plist.index(pl))

    return True

def findRelPathInSearchPath(spath, plist=None, **kargs):
    """Searches the list for matching objects in side-branches.

    Searches the paths provided by plist for hooks(pathx[-1]) 
    suitable to 'spath', which are entry points for specific 
    extension branches.
    
    The parameters of type 'is' are recommended when the 
    iterator is applied. This enhances the performance vs. 
    the post filtering.
    
    Args:
        spath:=(literal|glob): A path to be hooked into 
            'plist[]' when present. Could be either a 
            literal, or a glob as an relative or absolute
            path. Valid scope types:

                * literal : X
                * re      : -
                * glob    : X

            See common options for details.

        plist: List of potential hooks for 'spath'.
            See common options for details.

            default := sys.path

        **kargs:
            ias: Treats for local file names any 
                number of subsequent '/' only as one.

            isDir: Is a directory.

            isFile: Is a file.

            isLink: Is a symbolic link.

            isPathByLink: Has a symbolic link in path.

            matchidx=#idx: Ignore matches '< #idx', 
                return match '== #idx'. Depends on
                'reverse'

                default := 0 # first match

            noglob: Suppress application of 'glob'.

            not: Inverts to does not matched defined
                criteria.

            raw: Suppress normalization by call of 
                'os.path.normpath'.

            reverse: Reversed search order.

    Returns:
        When successful returns the absolute pathname, 
        else 'None'. For a list refer to iterator.

    Raises:
        passed through exceptions:
        
    """
    if type(plist) == NoneType:
        plist = sys.path

    raw = False
    ias = False
    _rgx = False
    _rev = False
    matchidx = 0

    _chkT = False
    _isL = False
    _isD = False
    _isF = False
    _isPL = False
    
    _not = False
    _ng = False

    for k, v in kargs.items():
        if k == 'matchidx':
            if not type(v) is int or v < 0:
                raise FileSysObjectsException("Requires int>0 matchidx=" + str(v))
            matchidx = v
        elif k == 'ias':
            ias = v
        elif k == 'not':
            _not = v
        elif k == 'raw':
            raw = v
        elif k == 'reverse':
            _rev = v
        elif k == 'noglob':
            _ng = v
        elif k == 'isLink':
            _chkT = True
            _isL = v
        elif k == 'isDir':
            _chkT = True
            _isD = v
        elif k == 'isFile':
            _chkT = True
            _isF = v
        elif k == 'isPathByLink':
            _chkT = True
            _isPL = v
        else:
            raise FileSysObjectsException("Unknown param: " + str(k) + ":" + str(v))

    # use canonical copy
    if not raw:
        if spath[-1] == os.sep:
            sp = os.path.normpath(spath) + os.sep
        else:
            sp = os.path.normpath(spath)

        if ias:
            sp = os.sep + sp.lstrip(os.sep) 

    if spath and len(spath) > 6 and spath[0:7] == 'file://':
        _sp = os.sep + spath[7:].lstrip(os.sep) 
    else:
        _sp = spath[:]
        
    def _checkit(p):
        _b = True

        if _chkT:
            if _isF and not os.path.isfile(_px):
                _b = False
            if _isD and not os.path.isdir(_px):
                _b = False
            if _isL and not os.path.islink(_px):
                _b = False
            if _isPL and not os.path.isfile(_px):
                _b = False
        return _b

    # short it up for absolute input of existing paths, thus is a literal too!
    if os.path.isabs(_sp) and os.path.exists(_sp):  # exists as absolute    
        _b = _checkit(_sp)
        for p in plist:
            if not p:
                continue
            if p.startswith(_sp):
                
                _b &= True

                if _b and matchidx != 0:
                    _b = False
                    matchidx -= 1
                
                return os.path.normpath(_sp)

        if _b and not _not:
            return _sp

        return None

    # now look for hooks of relative paths in plist
    if _rev:
        _pl = reversed(plist)
    else:
        _pl = plist
    
    for p in _pl:
        if not p:
            continue
        _b = True
        
        if os.path.isabs(_sp):
            _px = normpathX(_sp)
        else:
            _px = normpathX(os.path.abspath(p + os.sep + _sp))

        if os.path.exists(_px):
            _b = _checkit(_px)

            if _b and matchidx != 0:
                _b = False
                matchidx -= 1
            
            if _b and not _not:
                return _px

            continue

        if not _ng:
            # try a glob
            for gm in glob.glob(_px):
                _b = _checkit(gm)
    
                if _b and matchidx != 0:
                    _b = False
                    matchidx -= 1
                
                if _b and not _not:
                    return gm
    
                continue
            
    return None

def findRelPathInSearchPathIter(spath, plist=None, **kargs):
    """Iterates all matches in plist, see findRelPathInSearchPath.
    """
    if type(plist) == NoneType:
        plist = sys.path

    for pl in plist:
        r = findRelPathInSearchPath(spath, [pl], **kargs)
        if r:
            yield r
    pass

def getTopFromPathString(spath, plist=None, **kargs):
    """Searches for a partial path in search paths from a provided list.

    Searches for a given path component by various constraints
    on each string of provided 'plist' until the match of a break 
    condition. The match is performed by default left-to-right, which 
    results in top-down scan of a path hierarchy, or right-to-left as 
    an upward bottom-up search.
    
    Performs string operations only, the file system is neither
    checked, not utilized. 
    
    Args:
        spath: A path to be added to 'plist'.
            See common options for details.
            
        plist: List of search strings for match.
            See common options for details.
        
            default := sys.path
         
        **kargs:
            abs: Return absolute path.

            hook: Returns the found part of the 'plist' 
                entry only.

            ias: Treats for local file names any 
                number of subsequent '/' only as one.

            includeapp: Includes appspecific into search.
                E.g. 
                    input   :   '//hostname/a/hostame/x/y/z'
                    not set => '//hostname/a/hostame'
                    set     => '//hostname'

            matchidx=#idx: Ignore matches '< #idx', 
                return match '== #idx'.

                default := 0 # first match

            matchlvl=#num: Increment of match
                for top node when multiple are in 
                the path. 

                See common options for details.

            matchlvlupward=#num: Increment of match
                for top node when multiple are in 
                the path. 

                See common options for details.

            pattern: Scope and type of match pattern.
                literal: Literal node by node match

                regnode: Match regular expression for 
                    individual nodes, implies no contained 
                    'os.sep' and no 'os.pathsep'

            patternlvl: Defines the level of subnodes of the search
                path to be resolved. The value 'full' forces a full match
                of 'spath' within a 'plist' item.               

            raw: Suppress normalization by call of 
                'os.path.normpath'.

            reverse: This reverses the resulting search order 
                 from bottom-up to top-down. Takes effect on
                 'redundant' only.

            split: Returns the splitted path prefix matched on search list,  
                and the relative sub path outside search list.

    Returns:
        When successful returns a path, else None.

        Returns by default the expanded pathname including the searched.
         
 

    Raises:
        passed through exceptions:
    """
    if type(plist) == NoneType:
        plist = sys.path
    elif type(plist) != list:
        raise FileSysObjectsException("Requires list argument:" + str(plist))

    _rev = False
    raw = False
    ias = False
    incap = False
    _abs= 0
    _hook= False
    _pat = 0
    _patlvl = 0
    matchlvl = 0
    matchlvlupward = -1
    matchidx = 0
    for k, v in kargs.items():
        if k == 'matchidx':
            if not type(v) is int or v < 0:
                raise FileSysObjectsException("Requires int>0 matchidx=" + str(v))
            matchidx = v
        elif k == 'matchlvl':
            if not type(v) is int or v < 0:
                raise FileSysObjectsException("Requires int>0 matchlvl=" + str(v))
            matchlvl = v
            matchlvlupward = -1
        elif k == 'matchlvlupward':
            if not type(v) is int or v < 0:
                raise FileSysObjectsException("Requires int>0 matchlvlupward=" + str(v))
            matchlvl = -1
            matchlvlupward = v
        elif k == 'ias':
            ias = True
            incap = False
        elif k == 'includeapp':
            incap = True
            ias = False
        elif k == 'raw':
            raw = True
        elif k == 'reverse':
            _rev = True
        elif k == 'abs':
            _abs = True
        elif k == 'hook':
            _hook = True
            _split = False
        elif k == 'split':
            _hook = False
            _split = True
        elif k == 'patternlvl':
            if not v == 'full' and ( not type(v) is int or v < 0 ): 
                raise FileSysObjectsException("Requires int>0 patternlvl=" + str(v))
            _patlvl = v
        elif k == 'pattern':
            if v == 'literal':
                _pat = 0
            elif v == 'regnode':
                _pat = 1
#             elif v == 'all':
#                 _pat = 2
        else:
            raise FileSysObjectsException("Unknown option: " + str(k) + ":" + str(v))
    
    def _comp(p, b):
#         if _pat == 2:
#             return a == b        
        if _pat == 1:
            if p == '*':  # assume a glob expression, thus terminate re-processing now
                return 
            pc = re.compile(ur'^' + p + ur'$')
            px = pc.match(b)         
            if px:
                return px.string[px.start():px.end()]         
        elif _pat == 0:
            if p == b:
                return b        

    # define processed portion, save prefix for later prepend on result
    if not raw:
        _rtype, _host, _share, sp = splitAppPrefix(spath, **{'rtype':True})
        _app_prefix = _rtype + _host
        if _share:
            if _app_prefix:
                _app_prefix += os.sep + _share
            else:
                _app_prefix = _share
    else:
        _app_prefix, sp = '', spath

    # normalize
    _sp_elems = splitAppPrefix(sp,**kargs)
    sp= getAppPrefixLocalPath(_sp_elems)

    sp = sp.split(os.sep)
    if sp and sp[-1] == '':
        sp = sp[:-1]

    # FIXME:
    if sp and sp[0] == '':  # is @root
        if len(sp) > 1:
            _contained = False
            for cx in plist: # initially check anchor #FIXME: for multiple-path-entries
                _cxe = splitAppPrefix(cx,**kargs)
                _cxe= getAppPrefixLocalPath(_sp_elems)
                if _cxe.startswith(os.sep+sp[1]):
                    _contained = True
            if not _contained : 
                return None
            sp = sp[1:]
    
    if _patlvl == 'full':
        _patlvl = len(sp)-1
        
    si0 = -1
    if _rev:
        _pl = reversed(plist)
    else:
        _pl = plist

    for sl in _pl:  # scan each path for sp
        si0 += 1
        if not sl:
            continue
        
        if not raw:  # canonical        
            # manage app paths - current network only
            _rtype, _host, _share, sl = splitAppPrefix(sl, **{'rtype':True})
            _prefix = _rtype + _host

            if _share:
                if _prefix:
                    _prefix += os.sep + _share
                else:
                    _prefix = _share

            if _app_prefix:
                if _app_prefix != _prefix:
                    continue
            # _prefix += _share
        else:
            _prefix = ''
        s = sl.split(os.sep)
        if s[0] == '':
            s = s[1:]
        if s[-1] == '':
            s = s[:-1]

        if matchlvlupward > -1:  # count reversed within the path nodes, this is not the index 
            _len = len(s)
            si = len(s)
            _fin = False
            _ucnt = 0
            for sx in reversed(s):  # check each dir separate
                si -= 1
                _match = False
                _fin = False

                if si == 0 and sp[0] == '':  # root dir
                    _c = sx
                else:
                    _c = _comp(sp[0], sx)
                m = -1
                if _c:
                    for spx in sp:
                        m += 1
                        if si + m >= _len:
                            _fin = True
                            break
                        _c = _comp(spx, s[si + m])
                        if si + m < _len and m < len(sp) and _c:
                            _match = True
                            if m <= len(sp) - 1:
                                _fin = True
                        else:
                            if _match:
                                _fin = True
                                break

                if _fin:
                    if _ucnt < matchlvlupward:
                        _ucnt += 1
                        continue
                    else:
                        _ucnt = 0
                    
                if _fin and m >= _patlvl:  # full match in front of pos m
                    if _hook:
                        _spx = ''
                    else:    
                        if _c and m == len(sp) - 1:
                            _spx = [_c]
                        else:
                            _spx = sp[m:]

                    if matchidx == 0:
                        _r = _prefix
                        if os.sep.join(s[:si + m]):
                            if _r or os.path.isabs(sl):
                                _r += os.sep
                            _r += os.sep.join(s[:si + m])
                        if _spx:
                            if _r:
                                _r += os.sep
                            _r += os.sep.join(_spx)
                        if not os.path.isabs(sl) and _abs:
                            return os.path.abspath(_r)
                        return _r
                    matchidx -= 1
        
        else:  # if matchlvl > -1:
            si = -1
            _fin = False
            _len = len(s)
            _dcnt = 0
            for sx in s:  # check each dir separate
                si += 1
                _match = False
                _fin = False

                if si == 0 and sp[0] == '':  # root dir
                    _c = sx
                else:
                    _c = _comp(sp[0], sx)
                if _c:
                    _match = True
                    _fin = len(sp) <= 1
                    m = 1
                    for spx in sp[1:]:
                        if si + m >= _len:
                            _fin = True
                            _c = ''
                            break
                        _c = _comp(spx, s[si + m])
                        if si + m < _len and m < len(sp) and _c:
                            _match = True
                            if m >= len(sp) - 1:
                                _fin = True
                        else:
                            if _match:
                                _fin = True
                                break
                        m += 1

                if _fin:
                    if _dcnt < matchlvl:
                        _dcnt += 1
                        continue
                    else:
                        _dcnt = 0
                    
                if _fin and m >= _patlvl:  # full match in front of pos m    
                    if _hook:
                        _spx = ''
                    else:    
                        if _c and m == len(sp) - 1:
                            _spx = [_c]
                        else:
                            _spx = sp[m:]
                    if matchidx == 0:
                        _r = _prefix
                        _j = os.sep.join(s[:si + m])
                        if _j:
                            if _r or os.path.isabs(sl):
                                _r += os.sep
                            _r += _j
                        if _spx:
                            if _r:
                                _r += os.sep
                            _r += os.sep.join(_spx)
                        if not os.path.isabs(sl) and _abs:
                            return os.path.abspath(_r)
                        return _r
                    matchidx -= 1
    return None

def getTopFromPathStringIter(spath, plist=None, **kargs):
    """Iterates all matches in plist,see getTopFromPathString.
    """
    if type(plist) == NoneType:
        plist = sys.path
    for pl in plist:
        r = getTopFromPathString(spath, [pl], **kargs)
        if r:
            yield r
    pass

def setUpperTreeSearchPath(start=None, top=None, plist=None, **kargs):
    """Extends the 'plist' based search by each subdirectory from 'start' on upward to 'top'.
    
    Prepends a set of search paths into plist. The set of search 
    paths contains of each directory beginning with provided start 
    position. The inserted path is normalized by default
    
    Args:
        start: Start components of a path string.
            See common options for details.
            Valid scope types:

                * literal : X
                * re      : -
                * blob    : -

            default := caller-file-position.
        
        top: End component of a path string.
            The node 'top' is included.
            Valid scope types:

                * literal : X
                * re      : -
                * blob    : -

            default := <same-as-start>

        plist: List to for the storage.
            See common options for details.
            
            default := sys.path

        **kargs:
            append: Appends the set of search paths.
            
            ias: Treats for local file names any 
                number of subsequent '/' only as one.

            matchidx=#idx: Ignore matches '< #idx', 
                adds match '== #idx' and returns.

                default := 0 # all

            matchcnt=#num: The maximal number of matches
                returned when multiple occur.

            matchlvl=#num: Increment of match
                for top node when multiple are in 
                the path. 

                See common options for details.

            matchlvlupward=#num: Increment of match
                for top node when multiple are in 
                the path. 

                See common options for details.

            noTypeCheck: Supress required identical types
                of 'top' and 'start'. As a rule of thum for current
                version, the search component has to be less
                restrictive typed than the searched. 
                The default applicable type matches are::

                     top    ¦ start
                    --------+---------------------
                     LFSYS  ¦ LFSYS, LDSYS, SHARE
                            | SMB, CIFS, IAS
                     LDSYS  ¦ LDSYS
                     SHARE  ¦ SHARE
                     SMB    ¦ SMB
                     CIFS   ¦ CIFS
                     IAS    ¦ IAS

                See common options for details.

            prepend: Prepends the set of search paths.
                This is default.

            raw: Suppress normalization by call of 
                'os.path.normpath'.

            relonly: The paths are inserted relative to the
                top node only. This is mainly for test 
                purposes. The intermix of relative and
                absolute path entries is not verified.

            reverse: This reverses the resulting search order 
                 from bottom-up to top-down.

            unique: Insert non-present only, else present
                entries are not checked, thus the search order
                is changed in general for 'prepend', while
                for 'append' the present still covers the new
                entry. 
            
    Returns:
        When successful returns 'True', else returns either 'False', 
        or raises an exception.

    Raises:
        passed through exceptions:
    """
    if type(plist) == NoneType:
        plist = sys.path
    
    _relo = False
    _matchcnt = 0
    _matchidx = 0
    
    setUpperTreeSearchPath._matchcnt = 0
    setUpperTreeSearchPath._matchidx = 0
    
    matchlvl = 0
    matchlvlupward = -1
    reverse = False
    unique = False
    prepend = True
    _tchk= True
    _raw = False
    _ias = False
    _split = False
    _sitem = False
    for k, v in kargs.items():
        if k == 'relonly':
            _relo = True
        elif k == 'matchcnt':
            if not type(v) is int:
                raise FileSysObjectsException("Digits only matchcnt:" + str(v))
            _matchcnt = v
        elif k == 'matchidx':
            if not type(v) is int:
                raise FileSysObjectsException("Digits only matchidx:" + str(v))
            _matchidx = v
        elif k == 'matchlvl':
            if not type(v) is int:
                raise FileSysObjectsException("Digits only matchlvl:" + str(v))
            matchlvl = v
        elif k == 'matchlvlupward':
            if not type(v) is int:
                raise FileSysObjectsException("Digits only matchlvlupward:" + str(v))
            matchlvlupward = v
        elif k == 'reverse':
            reverse = True
        elif k == 'unique':
            unique = True
        elif k == 'append':
            prepend = False
        elif k == 'prepend':
            prepend = True
        elif k == 'raw':
            _raw = True
        elif k == 'ias':
            _ias = True
        elif k == 'splitItems':
            _split = True
        elif k == 'singleitem':
            _sitem = True
        elif k == 'noTypeCheck':
            _tchk = False
        
    if matchlvl > 0:
        matchlvlupward = -1
        
    #
    # Prepare search path list
    # if decided to normalize, and whether to ignore leading '//'
    #
    if _raw:  # match basically literally
        if not _ias:
            _plst = plist
        else:
            _plst = []
            for i in plist:
                # normalize
                _elems = splitAppPrefix(i,**kargs)
                _plst.append(getAppPrefixLocalPath(_elems))
    else:  # normalize for safer match conditions
            _plst = []
            for i in plist:
                # normalize
                _elems = splitAppPrefix(i,**kargs)
                _plst.append(getAppPrefixLocalPath(_elems))

    #
    # 0. prep start dir
    #
    if start == '':
        raise FileSysObjectsException("Empty start:''")
    elif start == None:
        start = getCallerModuleFilePathName(2)  # caller file
    # normalize
    _start_elems = splitAppPrefix(start,**kargs)
    start = getAppPrefixLocalPath(_start_elems)
    # try a literal
    if not os.path.isabs(start):
        start = getCallerPathName(2)+os.sep+start
    if os.path.isfile(start):
        start = os.path.dirname(start)  # we need dir
    if not os.path.exists(start):
        raise FileSysObjectsException("Missing start:" + str(start)) 

    # 1. prep top dir

    # normalize
    if top == '':
        raise FileSysObjectsException("Empty top:''")
    elif top == None:
        top = getCallerModulePathName(2)  # caller file
    # normalize
    _top_elems = list(splitAppPrefix(top,**kargs))


    # ptype
    if _tchk:
        if _top_elems and _start_elems: 
            if _top_elems[0] != _start_elems[0]:
                
                #TODO: still to enhance..
                if _top_elems[0]  in ( 'LFSYS', ):
                    if os.path.realpath(_top_elems[3]):
                        pass
                    elif _start_elems[0] in ( 'LDSYS', 'LFSYS', ):
                        pass
                    else:
                        raise FileSysObjectsException("LFSYS combined with "+str(_start_elems[0])+" requires relative pathname for LFSYS, given: "+str(_top_elems[3]))
                    pass
                else:
                    raise FileSysObjectsException("This version requires compatible types: start("+str(_start_elems[0])+") =! top("+str(_top_elems[0])+")")

    # share
#     if _top_elems[2]: 
#         if _top_elems[2] != _start_elems[2]:
#             raise FileSysObjectsException("Top is not in start:" + str(_top_elems[2]) + " != " + str(_top_elems[2]))
#     else:
#         _top_elems[2]  = _start_elems[2] 

    # node
#     if _top_elems[1]: 
#         if _top_elems[1] != _start_elems[1]:
#             raise FileSysObjectsException("Top is not in start:" + str(_top_elems[1]) + " != " + str(_top_elems[1]))
#     else:
#         _top_elems[1] = _start_elems[1]

    # path
#     if not os.path.isabs(_top_elems[3]):
#         kargs['patternlvl'] = 'full'
#         _top_elems[3] = os.path.splitdrive(getTopFromPathString(_top_elems[3], [start],**kargs))[1]
# #        _top_elems[3] = os.path.splitdrive(getTopFromPathString(_top_elems[3], [start],**{'patternlvl':'full',}))[1]

#     if not _top_elems[1] and not _top_elems[2] and not os.path.isabs(_top_elems[3]):
#         top = _top_elems[3]
#     else:
#         top= getAppPrefixLocalPath(_top_elems)

    top= getAppPrefixLocalPath(_top_elems)


    # if absolute
    if os.path.isabs(top):
        if not os.path.exists(top):
                raise FileSysObjectsException("Top does not exist:" + str(top))
    
    #
    # start upward recursion now
    #

    def _addsub(x, pl=plist):
        """...same for all."""
        # >3: nonlocal _matchcnt
        if _matchcnt != 0 and _matchcnt <= setUpperTreeSearchPath._matchcnt:
            return
        if _matchidx != 0 and _matchidx != setUpperTreeSearchPath._matchidx:
            return

        if unique and x in pl or x in plist:
            return False
        if reverse:
            pl.append(x)
        else:
            pl.insert(0, x)
        setUpperTreeSearchPath._matchcnt += 1
        pass

    # find top
    if top:
        # FIXME:
        if top == '.':
            top = os.path.abspath(top)
        top = escapeFilePath(top)
        start = escapeFilePath(start)

        _sx = re.sub(_CPREP, r"\1", top)

        # for now works literally 
        a = start.split(top)
        if len(a) == 1:
            raise FileSysObjectsException("Top is not in start:" + str(top))

        if matchlvl >= len(a):  # check valid range
            raise FileSysObjectsException("Match count out of range:" + str(matchlvl) + ">" + str(len(a)))
        elif matchlvlupward > 0 and matchlvlupward >= len(a):  # check valid range
            raise FileSysObjectsException("Match count out of range:" + str(matchlvlupward) + ">" + str(len(a)))

    else:
        if matchlvl > 0:
            raise FileSysObjectsException("Match count out of range:" + str(matchlvl) + "> 0")
        if matchlvlupward > 0:
            raise FileSysObjectsException("Match count out of range:" + str(matchlvlupward) + "> 0")
        _addsub(start)
        return True



    #
    # so we have actually at least one top within valid range and a remaining sub-path - let us start
    #
    
    if a == ['', '']:  # top == start
        if matchlvl > 0:
            raise FileSysObjectsException("Match count out of range:" + str(matchlvl) + "> 0")
        if matchlvlupward > 0:
            raise FileSysObjectsException("Match count out of range:" + str(matchlvl) + "> 0")
        _addsub(start)
        return True

    elif a[0] == '':  # top is prefix
        _tpath = top

        if matchlvlupward >= 0:
            mcnt = len(a) - 1 - matchlvlupward
        else:
            mcnt = matchlvl

        _spath = top.join(a[mcnt + 1:])  # sub-path for search recursion

    else:
        
        # get index for requested number of ignored/contained matches
        if matchlvlupward >= 0:
            mcnt = len(a) - 1 - matchlvlupward
        else:
            mcnt = matchlvl + 1

        # set matched prefix and postfix
        if os.path.isabs(top):
            _tpath = top
            _spath = (os.sep + top + os.sep).join(a[mcnt:])  # sub-path for search recursion
        elif not a[mcnt-1]: # tail
            _tpath = (os.sep + top + os.sep).join(a[:mcnt]) 
            _spath = ''
        else:
            _tpath = (os.sep + top + os.sep).join(a[:mcnt]) + os.sep + top  # top path as search hook
            _spath = (os.sep + top + os.sep).join(a[mcnt:])  # sub-path for search recursion

    if _relo:  # relative paths, mainly for test
        curp = ''
    else:
        curp = unescapeFilePath(_tpath)
        curp = os.path.normpath(curp)
        if curp not in plist:  # insert top itself
            _addsub(curp)

    a = _spath.split(os.sep)
    if prepend:
        for p in a:
            if not p:
                continue
            curp = os.path.join(curp, p)
            _addsub(curp)
    else:
        _buf = []
        for p in a:
            if not p:
                continue
            curp = os.path.join(curp, p)
            _addsub(curp, _buf)
        plist.extend(_buf)

    return True

def splitAppPrefix(apstr, **kargs):
    """Splits application prefix from resource-path - IEEE-1003.1/SMB/CIFS
    
    The supported application type prefixes are as follows,
    for detailed information refer to the chapter
    **Syntax Elements** `[details] <path_syntax.html#syntax-elements>`_
      ::

        PREFIXKEY := (
             'file:///' + 2SEP + SPECIALNODE + varSEP + share-name 
           | 'file://'
           | 'smb://' + SPECIALNODE + varSEP + share-name
           | 2SEP  SPECIALNODE  [varSEP]
           | nSEP       
        )
        SPECIALNODE := (
           <networknode>
         )
         share-name := (
           1*80pchar  # see [MS-DTYP]
         )


    Args:
        apstr: A path containing an application part.

        **kargs:
            ias: Ignore application separator, this
                just normalizes the pathname by 
                eliminating the PREFIXKEY property.
    
            raw: Suppress any normalization.

            rtype: Displays raw type prefix.

            tpf: Target platform for the filepathname.

                win:   MS-Windows with os.sep= '\\'

                posix: POSIX  based, with os.sep = '/'

                keep: keeps as provides, also intermixed,
                    os.sep, just escapes '/'

                else: adapts to current os.sep, similar 
                    'os.path.normpath'

                cnp: cross native posix
    
                    emulates native behaviour of 'os.path.normpath' 
                    on posix platform, e.g.::
    
                        d:/  => d:
                        d:\\  => d:/
                
                cnw:cross native win
    
                    emulates native behaviour of 'os.path.normpath' 
                    on win platform, e.g.::
    
                        d:/  => d:/
                        d:\\  => d:
                
                else: adapt os.sep, local os native

    Returns:
        When split successful returns a tuple containing:
          ::

            (TYPE, host-name, share-name, pathname)
             
              TYPE := (SMB|SHARE|LFSYS|LDSYS)
                 SMB := ('file:///'+2SEP|'smb://')
                 SHARE := 2SEP
                 LFSYS := ('file://'|'') 
                 LDSYS := [a-z]':' 
              host-name =: (host-name|'')
              share-name := (valid-share-name|'')
              valid-share-name := (
                   smb-share-name
                 | cifs-share-name
                 | win-drive-share-name
                 | win-drive-os
                 | win-special-share-name
              )
              pathname := "pathname on target"
 
        else:
          ::

             (LFSYS, '', '', apstr)

        REMARK: The hostname may contain in current release
            any suboption, but is not tested with options at all.

    Raises:
        passed through exceptions:
    """
    ias = kargs.get('ias', False)
    raw = kargs.get('raw', False)
    rtype = kargs.get('rtype', False)
    
    if not raw:
        if ias:
            _cg = _COMPT.match(apstr)
            if _cg:
                return ('IAS', '', _cg.group(_cg.lastindex+2), normpathX(_cg.group(_cg.lastindex+3),**kargs),)

        for i in _COMPX.finditer(apstr):
            #
            #FIXME: i.lastindex
            #
            for g in _COMPXg:
                if i.group(g + 3) or i.group(g):  # 3:local file system 0:uri or IEEE/UNC/SMB
                    pass
                elif i.group(g + 2):  # 2:DOS-DRIVE - only
                    if not rtype:
                        return (PGTYPE[(g - 2) / 5], i.group(g + 1), i.group(g + 2), '')
                else:
                    continue  # should not occur, anyhow...
                if not rtype:
                    return (PGTYPE[(g - 2) / 5], i.group(g + 1), i.group(g + 2), normpathX(i.group(g + 3),**kargs))
                else: 
                    return (i.group(g), i.group(g + 1), i.group(g + 2), normpathX(i.group(g + 3),**kargs))
            return None
    else:
        if ias:
            _cg = _COMPT.match(apstr)
            if _cg:
                return ('IAS', '', _cg.group(_cg.lastindex+2), _cg.group(_cg.lastindex+3),)
        for i in _COMPX.finditer(apstr):
            for g in _COMPXg:
                if i.group(g + 3) or i.group(g):  # 3:local file system / 0:uri or IEEE/UNC/SMB
                    return (i.group(g), i.group(g + 1), i.group(g + 2), i.group(g + 3))
            return None
    return ('', apstr)

def getAppPrefixLocalPath(elems,**kargs):
    """Joins app elements to a path for local access.
    
    Args:
        elems: Elements as provided by 'splitAppPrefix' 

        **kargs:
            tpf: Target platform for the filepathname.

                win:   MS-Windows with os.sep= '\\'

                posix: POSIX  based, with os.sep = '/'

                cnp: cross native posix
    
                    emulates native behaviour of 'os.path.normpath' 
                    on posix platform, e.g.::
    
                        d:/  => d:
                        d:\\  => d:/
                
                cnw:cross native win
    
                    emulates native behaviour of 'os.path.normpath' 
                    on win platform, e.g.::
    
                        d:/  => d:/
                        d:\\  => d:
                
                cnp: cross native posix
    
                    emulates native behaviour of 'os.path.normpath' 
                    on posix platform, e.g.::
    
                        d:/  => d:
                        d:\\  => d:/
                
                cnw:cross native win
    
                    emulates native behaviour of 'os.path.normpath' 
                    on win platform, e.g.::
    
                        d:/  => d:/
                        d:\\  => d:
                
                else: adapt os.sep, local os native

    Returns:
        When access path when successful, else None.

    Raises:
        passed through exceptions:
    """
    _tpf = kargs.get('tpf',False)

    if _tpf in ('Windows', 'win',):
        s = '\\'
    elif _tpf == 'posix':
        s = '/'
    else:
        s = os.sep

    ret = ''
    if elems and elems[1]:
        if not elems[2]:
            if platform.system() == 'Windows' and elems[0] not in ('SMB','SHARE'):
                raise FileSysObjectsException("Missing share name for start="+str(elems))
        ret += 2*s+elems[1]
    if elems and elems[2]:
        if elems[1]:
            ret += s+elems[2]
        else:
            ret += elems[2]
    if elems and ret:
        if ( elems[1] or elems[2] ) and elems[3][0] not in ('/','\\',os.sep):
            ret += s+elems[3]
        else:
            ret += elems[3]
    elif elems:
        ret += elems[3]
    
    return ret    


#***
# Static 're' components
#
# match pattern for path names - could be applied on any OS, 
# but required mandatory on MS-Windows
#
alist= [                                 # escapes path names

    r'((?<![\\\\])[\\\\]*([\a]))',            # controls of 're' and others
    r'((?<![\\\\])[\\\\]*([\b]))',#4
    r'((?<![\\\\])[\\\\]*([\f]))',
    r'((?<![\\\\])[\\\\]*([\n]))',
    r'((?<![\\\\])[\\\\]*([\r]))',   #10
    r'((?<![\\\\])[\\\\]*([\t]))',
    r'((?<![\\\\])[\\\\]*([\v]))',

    r'(^(file://///)(?![/\\\\]))',                   # some URIs, suppress slash reduction 
    r'(^(file:///[\\][\\])(?![/\\\\]))',                   # some URIs, suppress slash reduction 
    r'(^(file://[\\][\\])(?![/\\\\]))',   #20           # some URIs, suppress slash reduction 
    r'(^(file://))',       
    r'(^(smb://))',  #24   
    r'(^(cifs://))',     
    r'(^(ias://))',                       #      special, proprietary for test purposes     

    r'(^([\\\\][\\\\])(?![\\\\]))',  #30    # os.sep on win
    r'((^[\\\\]+)$)',
    
    r'(([\\\\]+[.][\\\\]+))',
    r'(([\\\\]+[.]$))',
    r'((^[.][\\\\]+))',
    
    r'((?<=[a-zA-Z]:)([\\\\]+)$)',  #40
    r'((?<![\\\\])([\\\\]+)$)',
    r'((?<![\\\\])([\\\\][\\\\])(?![\\\\]))', 
    r'((?<![\\\\])([\\\\]+)(?![\\\\]))',
    r'(^([\\\\])(?![\\\\]))',

    r'(^(//)(?!/))',        #50             # os.sep on Linux, UNIX, OS-X
    r'(^(/)$)',

    r'(([^/]+/+\.\./*))',
    r'((?<=[^/])(/+[^/]+/+\.\.))',
    r'(([^/]+/+\.\./+))',
    r'((?=[^.]*)(\.\./+))', #60 
    
    r'((/+[.])+/*$)', 
    r'((/+[.]/+))', 
    r'((?=[^.]*)(\./+))', 

    r'(^(///+)(?!/))', 
    r'((?<=[a-zA-Z]:)(/+)$)', #70 
    r'((/+)(?:$))', 
    r'((/+)(?![/]))', 

]
_rx = re.compile('|'.join(alist))

#
# map matches to actual controlsequneces
#
DOIT = 11111 # out of range
ASCII_CTRL = {
    2 :  '\a',
    4 :  '\b',
    6 :  '\f',
    8 :  '\n',
    10 :  '\r', 
    12 :  '\t',
    14 :  '\v',

    16 :  r'file://///',
    18 :  r'file:///\\',
    20 :  r'file://\\',
    22 :  'file://',
    24 :  'smb://',
    26 :  'cifs://',
    28 :  'ias://',
    
    30:  '\\\\',
    32 :  DOIT,
    34 :  DOIT,
    36 :  DOIT,
    38 :  DOIT,
    40 :  DOIT,
    42 :  DOIT,
    44 :  '\\\\',
    46 :  DOIT,
    48 :  '\\',

    50 :  DOIT,
    52 :  DOIT,
    54 :  DOIT,
    56 :  DOIT,
    58 :  DOIT,
    60 :  DOIT,
    62 :  DOIT,
    64 :  DOIT,
    66 :  DOIT,
    68 :  DOIT,
    70 :  DOIT,
    72 :  DOIT,
    74 :  DOIT,
}

#
# map matches to appropriate replacement
#

#*
#* *** cross native posix - slash *** emulates normpath on win for remote posix
#*
ASCII_REPLACE_CNP = {
    2 :    r'/a',
    4 :    r'/b',
    6 :    r'/f',
    8 :    r'/n',
    10 :  r'/r',
    12 :  r'/t',
    14 :  r'/v',

    16 :  'file://///',
    18 :  'file://///',
    20 :  'file://///',
    22 :  'file://',
    24 :  'smb://',
    26 :  'cifs://',
    28 :  'ias://',

    30 :  r'//',
    32 :  r'/',
    34 :  r'/',
    36 :  r'/',
    38 :  r'/',
    40 :  '',
    42 :  '',
    44 :  r'/',
    46 :  r'/',
    48 :  r'/',
    
    50 :  '//',
    52 :  '/',
    54 :  '',
    56 :  '',
    58 :  '',
    60 :  '/',
    62 :  '',
    64 :  '/',
    66 :  '',
    68 :  '/',
    70 :  '/',
    72:  '',
    74 :  '/',
}

#*
#* *** cross native win - backslash *** emulates normpath on posix for remote win
#*
ASCII_REPLACE_CNW = {
    2 :    r'\\a',
    4 :    r'\\b',
    6 :    r'\\f',
    8 :    r'\\n',
    10 :  r'\\r',
    12 :  r'\\t',
    14 :  r'\\v',

    16 :  r'file://///',
    18 :  r'file:///\\\\',
    20 :  r'file://\\\\',
    22 :  'file://',
    24 :  'smb://',
    26 :  'cifs://',
    28 :  'ias://',

    30 :  r'\\\\',
    32 :  r'\\',
    34 :  r'\\',
    36 :  r'\\',
    38 :  r'\\',

    40 :  r'\\',
    42 :  '',
    44 :  r'\\',
    46 :  r'\\',
    48 :  r'\\',

    50 :  r'\\\\',
    52 :  r'\\',
    54 :  r'',
    56 :  r'',
    58 :  r'',
    60 :  r'\\',
    62 :  r'',
    64 :  r'\\',
    66 :  r'',
    68 :  r'\\',
    70 :  r'',
    72 :  '',
    74 :  r'\\',
}

#*
#* *** keep ***
#*
ASCII_REPLACE_K = {
    2 :    r'\\a',
    4 :    r'\\b',
    6 :    r'\\f',
    8 :    r'\\n',
    10 :  r'\\r',
    12 :  r'\\t',
    14 :  r'\\v',

    16 :  r'file://///',
    18 :  r'file:///\\\\',
    20 :  r'file://\\\\',
    22 :  'file://',
    24 :  'smb://',
    26 :  'cifs://',
    28 :  'ias://',

    30 :  r'\\\\',
    32 :  r'\\',
    34 :  r'\\',
    36 :  r'\\',
    38 :  r'\\',

    40 :  r'\\',
    42 :  '',
    44 :  r'\\',
    46 :  r'\\',
    48 :  r'\\',

    50 :  '//',
    52 :  '/',
    54 :  '',
    56 :  '',
    58 :  '',
    60 :  '/',
    62 :  '',
    64 :  '/',
    66 :  '',
    68 :  '/',
    70 :  '/',
    72 :  '',
    74 :  '/',
}
#*
#* *** replace with backslash ***
#*
ASCII_REPLACE_B = {
    2 :    r'\\a',
    4 :    r'\\b',
    6 :    r'\\f',
    8 :    r'\\n',
    10 :  r'\\r',
    12 :  r'\\t',
    14 :  r'\\v',

    16 :  r'file://///',
    18 :  r'file:///\\\\',
    20 :  r'file://\\\\',
    22 :  'file://',
    24 :  'smb://',
    26 :  'cifs://',
    28 :  'ias://',

    30 :  r'\\\\',
    32 :  r'\\',
    34 :  r'\\',
    36 :  r'\\',
    38 :  r'\\',

    40 :  r'\\',
    42 :  '',
    44 :  r'\\',
    46 :  r'\\',
    48 :  r'\\',

    50 :  r'\\\\',
    52 :  r'\\',
    54 :  r'',
    56 :  r'',
    58 :  r'',
    60 :  r'\\',
    62 :  r'',
    64 :  r'\\',
    66 :  r'',
    68 :  r'\\',
    70 :  r'\\',
    72 :  '',
    74 :  r'\\',
}

#*
#* *** replace with slash ***
#*
ASCII_REPLACE_S= {
    2 :    r'/a',
    4 :    r'/b',
    6 :    r'/f',
    8 :    r'/n',
    10 :  r'/r',
    12 :  r'/t',
    14 :  r'/v',

    16 :  'file://///',
    18 :  'file://///',
    20 :  'file://///',
    22 :  'file://',
    24 :  'smb://',
    26 :  'cifs://',
    28 :  'ias://',

    30 :  r'//',
    32 :  r'/',
    34 :  r'/',
    36 :  r'/',
    38 :  r'/',
    40 :  r'/',
    42 :  '',
    44 :  r'/',
    46 :  r'/',
    48 :  r'/',
    
    50 :  '//',
    52 :  '/',
    54 :  '',
    56 :  '',
    58 :  '',
    60 :  '/',
    62 :  '',
    64 :  '/',
    66 :  '',
    68 :  '/',
    70 :  '',
    72:  '',
    74 :  '/',
}

def sub_esc_keep(it):
    """To be used by re.sub() - keeps mixed
    """
    g = it.lastindex+1
    if it.group(g):
        x = it.group(g)
        c = ASCII_CTRL.get(g)              # evtl. drop these in release
        if c == DOIT or c == it.group(g):  # evtl. drop these in release
            x = ASCII_REPLACE_K[g]
        return x

def sub_esc_b(it):
    """To be used by re.sub() - converts to backslash
    """
    g = it.lastindex+1
    if it.group(g):
        x = it.group(g)
        c = ASCII_CTRL.get(g)              # evtl. drop these in release
        if c == DOIT or c == it.group(g):  # evtl. drop these in release
            x = ASCII_REPLACE_B[g]
        return x

def sub_esc_s(it):
    """To be used by re.sub() - converts to slash
    """
    g = it.lastindex+1
    if it.group(g):
        x = it.group(g)
        c = ASCII_CTRL.get(g)              # evtl. drop these in release
        if c == DOIT or c == it.group(g):  # evtl. drop these in release
            x = ASCII_REPLACE_S[g]
        return x

def sub_esc_cnw(it):
    """To be used by re.sub() - converts to slash
    """
    g = it.lastindex+1
    if it.group(g):
        x = it.group(g)
        c = ASCII_CTRL.get(g)              # evtl. drop these in release
        if c == DOIT or c == it.group(g):  # evtl. drop these in release
            x = ASCII_REPLACE_CNW[g]
        return x

def sub_esc_cnp(it):
    """To be used by re.sub() - converts to slash
    """
    g = it.lastindex+1
    if it.group(g):
        x = it.group(g)
        c = ASCII_CTRL.get(g)              # evtl. drop these in release
        if c == DOIT or c == it.group(g):  # evtl. drop these in release
            x = ASCII_REPLACE_CNP[g]
        return x

def escapeFilePath(p,tps=None):
    """Normalize 'os.sep' by re module.

    Considers any os.sep seperated item as path part.
    Manages os.sep including flags of 're' as special 
    characters,e.g. 'a', 'b', and 'x'.

    Args:
        p: A path.
        
        tps: Target path seperator:

            s: slash

            b: backslash

            k: keep 
                
                keeps, also intermixed, just escapes backslash
                
            cnp: cross native posix

                emulates native behaviour of 'os.path.normpath' 
                on posix platform, e.g.::

                    d:/  => d:
                    d:\\  => d:/
            
            cnw:cross native win

                emulates native behaviour of 'os.path.normpath' 
                on win platform, e.g.::

                    d:/  => d:/
                    d:\\  => d:
            
            else: adapt os.sep, local os native

    Returns:
        Path.
    """
    if tps not in ('s','b','k', 'cnw', 'cnp', ):
        if platform.system() == 'Windows':
            return _rx.sub(sub_esc_b, p)
        else:
            return _rx.sub(sub_esc_s, p)
        
    if tps == 's':
        return _rx.sub(sub_esc_s, p)
    elif tps == 'b':
        return _rx.sub(sub_esc_b, p)
    elif tps == 'k':
        return _rx.sub(sub_esc_keep, p)
    elif tps == 'cnw':
        return _rx.sub(sub_esc_cnw, p)
    elif tps == 'cnp':
        return _rx.sub(sub_esc_cnp, p)
    
    # just for the paranoid...
    return _rx.sub(sub_esc_keep, p)

#***
#* Static 're' components for table driven remapping
#*

# match pattern for path names - could be applied on any OS, 
# but required mandatory on MS-Windows
#
blist= [
    r'((?<![\\\\])¦(?=^)([\\\\][\\\\][a]))',  #2
    r'((?<![\\\\])¦(?=^)([\\\\][\\\\][b]))',
    r'((?<![\\\\])¦(?=^)([\\\\][\\\\][f]))',
    r'((?<![\\\\])¦(?=^)([\\\\][\\\\][n]))',
    r'((?<![\\\\])¦(?=^)([\\\\][\\\\][r]))',  #10
    r'((?<![\\\\])¦(?=^)([\\\\][\\\\][t]))',
    r'((?<![\\\\])¦(?=^)([\\\\][\\\\][v]))',

    r'(^(file:///[\\][\\][\\][\\])(?![/\\\\]))',                   # some URIs, suppress slash reduction 
    r'(^(file://[\\][\\][\\][\\])(?![/\\\\]))',   #18           # some URIs, suppress slash reduction 

    r'(^([\\\\][\\\\][\\\\][\\\\])(?![\\\\]))', #20
    r'(^([\\\\][\\\\])(?![\\\\]))',
    r'((?<![\\\\])([\\\\][\\\\][\\\\][\\\\])$)',  
    r'((?<![\\\\])([\\\\][\\\\][\\\\][\\\\])(?![\\\\]))',
    r'((?<![\\\\])([\\\\][\\\\])$)',
    r'((?<![\\\\])([\\\\][\\\\])(?![\\\\]))', #30
]
_ry = re.compile('|'.join(blist))
#
# map matches to actual controlsequneces
#
ASCII_ESC = {
    2 :    r'\\a',
    4 :    r'\\b',
    6 :    r'\\f',
    8 :    r'\\n',
    10 :  r'\\r',
    12 :  r'\\t',
    14 :  r'\\v',
    
    16 :  r'file:///\\\\',
    18 :  r'file://\\\\',

    20 :  r'\\\\',
    22:   r'\\',
    24 :  r'\\\\',
    26 :  r'\\\\',
    28 :  r'\\',
    30 :  r'\\',
}
 
#
# map matches to appropriate replacement
#
ASCII_DEESC = {
    2 :  '\a',
    4 :  '\b',
    6 :  '\f',
    8 :  '\n',
    10 :  '\r',
    12 :  '\t',
    14 :  '\v', 
      
    16 :  r'file:///\\',
    18 :  r'file://\\',

    20 :  r'\\',
    22 : '\\',
    24:  r'\\',
    26 : '\\',
    28 : '\\',
    30  :  '\\',
}
def sub_unesc(it):
    """To be used by re.sub()
    """
    g = it.lastindex+1
    if it.group(g):
        x = it.group(g)
        c = ASCII_ESC.get(g)    # evtl. drop these in release
        if c == it.group(g):    # evtl. drop these in release
            x = ASCII_DEESC[g]
        return x

def unescapeFilePath(p):
    """Unescape 'os.pathsep' by re module.

    Considers any os.pathsep as path part.
    Manages os.pathsep only - thus flags of
    the re module itself are not considered
    and may omitted in regular expressions
    for pathnames, e.g. 'a', 'b', and 'x'.

    Args:
        p: A path.

    Returns:
        Path.
    """
    return _ry.sub(sub_unesc, p)

def normpathX(p,**kargs):
    """Normalize path similar to re module.

    Considers all os.sep and os.pathsep of supported
    as valid path characters and treats tem as reserved characters.

    In advance of os.path.normpath this supports the following simple
    URIs:
        smb, cifs, file
    
    Args:
        p: A path.

        **kargs:
            tpf: Target platform for the filepathname.

                win:   MS-Windows with os.sep= '\\'

                posix: POSIX  based, with os.sep = '/'

                keep: Keeps as provided, also intermixed,
                    os.sep, just escapes '/'

                else: similar to 'os.path.normpath', 
                    transforms to current 'os.sep'

                cnp: cross native posix
    
                    emulates native behaviour of 'os.path.normpath' 
                    on posix platform, e.g.::
    
                        d:/  => d:
                        d:\\  => d:/
                
                cnw:cross native win
    
                    emulates native behaviour of 'os.path.normpath' 
                    on win platform, e.g.::
    
                        d:/  => d:/
                        d:\\  => d:
                
                else: adapt os.sep, local os native

    Returns:
        Path.
    """
    tpf = kargs.get('tpf',platform.system())
    if tpf in ('Windows', 'win',):
        p = escapeFilePath(p,'b')
        p = unescapeFilePath(p)
    elif tpf == 'posix':
        p = escapeFilePath(p,'s')
        p = unescapeFilePath(p)
    elif tpf == 'keep':
        p = escapeFilePath(p,'k')
        p = unescapeFilePath(p)

    elif tpf == 'cnw':
        p = escapeFilePath(p,'cnw')
        p = unescapeFilePath(p)
    elif tpf == 'cnp':
        p = escapeFilePath(p,'cnp')
        p = unescapeFilePath(p)

    else:
        p = escapeFilePath(p,)
        p = unescapeFilePath(p)
    return p
