# This file is part of hgnested.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
'''commands to manage nested repositories.

This extension provides commands that apply to all the nested repositories.

It was inspired by the forest extension by Robin Farine.
'''

import os
import time
from functools import partial
from mercurial import hg
from mercurial import commands, localrepo, hgweb
from mercurial import util
from mercurial import cmdutil
from mercurial import extensions
from mercurial import wireproto
from mercurial.error import CapabilityError
from mercurial.scmutil import walkrepos
from mercurial.i18n import _

__version__ = '0.8'
testedwith = '3.6 3.7 3.8 3.9'
buglink = 'https://bitbucket.org/cedk/hgnested/issues'

cmdtable = {}
command = cmdutil.command(cmdtable)

_nested_cache = {}
_nested_refreshinterval = 20


def _capabilities(orig, repo, proto):
    caps = orig(repo, proto)
    caps.append('nested')
    return caps
extensions.wrapfunction(wireproto, '_capabilities', _capabilities)


@wireproto.wireprotocommand('nested')
def nested(repo, proto):
    '''Return a list of nested repositories.'''
    return "\n".join(repo.nested)


def reposetup(ui, repo):
    if isinstance(repo, localrepo.localrepository):
        class nestedrepo(repo.__class__):
            @property
            def nested(self):
                '''Return a list of nested repositories.'''
                cache = _nested_cache.setdefault(self.root, {
                    'lastrefresh': 0,
                    'nested': None,
                    })
                if (cache['lastrefresh'] + _nested_refreshinterval
                        > time.time()):
                    return cache['nested']
                res = {}
                paths = [self.root]
                while paths:
                    path = paths.pop()
                    if os.path.realpath(path) in res:
                        continue
                    for root, dirs, files in os.walk(path):
                        realroot = os.path.realpath(root)
                        absroot = os.path.abspath(root)
                        for dir in dirs[:]:
                            if dir == '.hg':
                                res[realroot] = absroot
                                proot = os.path.join(root, '.hg', 'patches')
                                if os.path.isdir(os.path.join(proot, '.hg')):
                                    realproot = os.path.realpath(proot)
                                    absproot = os.path.abspath(proot)
                                    res[realproot] = absproot
                                dirs.remove('.hg')  # Don't visit .hg directory
                            else:
                                path = os.path.join(root, dir)
                                if (os.path.islink(path)
                                        and os.path.realpath(path) not in res):
                                    paths.append(path)
                prefix = len(self.root) + 1
                res = [x[prefix:] or '.' for x in res.itervalues()]
                res.sort()
                cache['nested'] = res
                cache['lastrefresh'] = time.time()
                return res
        repo.__class__ = nestedrepo

    if isinstance(repo, wireproto.wirepeer):
        class nestedwirepeer(repo.__class__):
            @property
            def nested(self):
                '''Return a list of nested repositories.'''
                if not self.capable('nested'):
                    raise util.Abort(_("Remote repository doesn't support "
                        "the nested extension."))
                return self._call('nested').splitlines()
        repo.__class__ = nestedwirepeer


def _hgwebdir_refresh(orig, self):
    refreshinterval = 20
    if self.ui:
        refreshinterval = self.ui.configint('web', 'refreshinterval',
            refreshinterval)
    if self.lastrefresh + refreshinterval > time.time():
        return
    orig(self)
    for prefix, root in self.ui.configitems('collections'):
        prefix = util.pconvert(prefix)
        for path in walkrepos(root, followsym=True):
            repo = hg.repository(self.ui, path)
            for npath in repo.nested:
                npath = os.path.normpath(os.path.join(path, npath))
                name = util.pconvert(npath)
                if name.startswith(prefix):
                    name = name[len(prefix):]
                repo = (name.lstrip('/'), npath)
                if repo not in self.repos:
                    self.repos.append(repo)
    self.lastrefresh = time.time()
extensions.wrapfunction(
    hgweb.hgwebdir_mod.hgwebdir, 'refresh', _hgwebdir_refresh)


def _nested_apply(ui, repo, function, status, *args, **kwargs):
    'Apply function to all nested repositories'
    for npath in repo.nested:
        if npath == '.':
            nrepo = repo
            lui = ui
        else:
            lpath = os.path.join(repo.root, npath)
            nrepo = hg.repository(ui, lpath)
            lui = nrepo.ui
            if function is _nested_diff:
                kwargs['prefix'] = npath
        if status:
            lui.status('[%s]\n' % npath)
        function(lui, nrepo, *args, **kwargs)
        if status:
            lui.status('\n')


def _nested_diff(ui, repo, *pats, **opts):
    diffordiffstat = cmdutil.diffordiffstat
    cmdutil.diffordiffstat = partial(diffordiffstat,
        prefix=opts.get('prefix') or '')
    commands.diff(ui, repo, *pats, **opts)
    cmdutil.diffordiffstat = diffordiffstat


@command('^ndiff', cmdutil.findcmd('diff', commands.table)[1][1],
    _('[OPTION]... ([-c REV] | [-r REV1 [-r REV2]]) [FILE]...'))
def ndiff(ui, repo, *pats, **opts):
    '''diff nested repositories (or selected files)

    Show differences between revisions for the specified files.

    Look at the help of diff command for more informations.'''
    _nested_apply(ui, repo, _nested_diff, False, *pats, **opts)


@command('^nclone', cmdutil.findcmd('clone', commands.table)[1][1],
    _('[OPTION]... SOURCE [DEST]'), norepo=True)
def nclone(ui, source, dest=None, **opts):
    '''make a copy of an existing repository and all nested repositories

    Create a copy of an existing repository in a new directory.

    Look at the help of clone command for more informations.'''
    origsource = ui.expandpath(source)
    remotesource, remotebranch = hg.parseurl(origsource, opts.get('branch'))
    if hasattr(hg, 'peer'):
        remoterepo = hg.peer(ui, opts, remotesource)
        localrepo = remoterepo.local()
        if localrepo:
            remoterepo = localrepo
    else:
        remoterepo = hg.repository(hg.remoteui(ui, opts), remotesource)
    if dest is None:
        dest = hg.defaultdest(source)
        ui.status(_("destination directory: %s\n") % dest)
    for npath in remoterepo.nested:
        if npath == '.':
            npath = ''
        u = util.url(source)
        if u.scheme:
            nsource = '%s/%s' % (source, npath)
        else:
            nsource = os.path.join(source, npath)
        ndest = os.path.join(dest, npath)
        ui.status('[%s]\n' % os.path.normpath(
            os.path.join(os.path.basename(dest),
                ndest[len(dest) + 1:])))
        commands.clone(ui, nsource, dest=ndest, **opts)
        ui.status('\n')


@command('^nshare',
    [('U', 'noupdate', None, _('do not create a working copy'))],
    _('[-U] SOURCE [DEST]'), norepo=True)
def nshare(ui, source, dest=None, noupdate=False):
    '''create a new shared repository and all nested repositories
    '''
    sourcerepo = hg.repository(ui, source)
    if dest is None:
        dest = hg.defaultdest(source)
        ui.status(_("destination directory: %s\n") % dest)
    for npath in sourcerepo.nested:
        if npath == '.':
            npath = ''
        u = util.url(source)
        if u.scheme:
            nsource = '%s/%s' % (source, npath)
        else:
            nsource = os.path.join(source, npath)
        ndest = os.path.join(dest, npath)
        ui.status('[%s]\n' % os.path.normpath(
            os.path.join(os.path.basename(dest),
                ndest[len(dest) + 1:])))
        hg.share(ui, nsource, ndest, not noupdate)
        ui.status('\n')


@command('nincoming|nin', cmdutil.findcmd('incoming', commands.table)[1][1],
    _('[-p] [-n] [-M] [-f] [-r REV]... [--bundle FILENAME] [SOURCE]'))
def nincoming(ui, repo, dest=None, **opts):
    '''show changest not found in repository and all nested repositories

    Look at the help of incoming command for more informations.'''
    _nested_apply(ui, repo, commands.incoming, True, dest=dest, **opts)


@command('noutgoing|nout', cmdutil.findcmd('outgoing', commands.table)[1][1],
    _('[-M] [-p] [-n] [-f] [-r REV]... [DEST]'))
def noutgoing(ui, repo, dest=None, **opts):
    '''show changesest not found in the destination and all nested repositories

    Look at the help of outgoing command for more informations.'''
    _nested_apply(ui, repo, commands.outgoing, True, dest=dest, **opts)


@command('npull', cmdutil.findcmd('pull', commands.table)[1][1],
    _('[-u] [-f] [-r REV]... [-e CMD] [--remotecmd CMD] [SOURCE]'))
def npull(ui, repo, source="default", **opts):
    '''pull changes from the specified source and all nested repositories

    Pull changes from a remote repository to a local one.

    Look at the help of pull command for more informations.'''
    def test(ui, repo, source, **opts):
        source, branches = hg.parseurl(ui.expandpath(source),
                opts.get('branch'))
        other = hg.repository(hg.remoteui(repo, opts), source)
        revs, checkout = hg.addbranchrevs(repo, other, branches,
                opts.get('rev'))
        if revs:
            try:
                revs = [other.lookup(rev) for rev in revs]
            except CapabilityError:
                err = _("Other repository doesn't support revision lookup, "
                        "so a rev cannot be specified.")
                raise util.Abort(err)
    if (source != 'default'
            or opts.get('branch')
            or opts.get('rev')):
        _nested_apply(ui, repo, test, False, source=source, **opts)
    _nested_apply(ui, repo, commands.pull, True, source=source, **opts)


@command('^npush', cmdutil.findcmd('push', commands.table)[1][1],
    _('[-f] [-r REV]... [-e CMD] [--remotecmd CMD] [DEST]'))
def npush(ui, repo, dest=None, **opts):
    '''push changes to the specified destination and all nested repositories

    Push changes from the local repository to the specified destination.

    Look at the help of status command for more informations.'''
    def test(ui, repo, dest=None, **opts):
        dest = ui.expandpath(dest or 'default-push', dest or 'default')
        dest, branches = hg.parseurl(dest, opts.get('branch'))
        revs, checkout = hg.addbranchrevs(repo, repo, branches,
                opts.get('rev'))
        if hasattr(hg, 'peer'):
            other = hg.peer(ui, opts, dest)
            localother = other.local()
            if localother:
                other = localother
        else:
            other = hg.repository(hg.remoteui(repo, opts), dest)
        if revs:
            revs = [other.lookup(rev) for rev in revs]
    _nested_apply(ui, repo, test, False, dest=dest, **opts)
    _nested_apply(ui, repo, commands.push, True, dest=dest, **opts)


@command('^nstatus|nst', cmdutil.findcmd('status', commands.table)[1][1],
    _('[OPTION]... [FILE]...'))
def nstatus(ui, repo, *pats, **opts):
    '''show changed files in the working directory and all nested repositories

    Show status of files in the repository.

    Look at the help of status command for more informations.'''
    _nested_apply(ui, repo, commands.status, True, *pats, **opts)


@command('^nupdate|nup', cmdutil.findcmd('update', commands.table)[1][1],
    _('[-c] [-C] [-d DATE] [[-r] REV]'))
def nupdate(ui, repo, node=None, rev=None, clean=False, date=None, check=False,
        **opts):
    '''update working directory and all nested repositories

    Update the repository's working directory to the specified changeset.

    Look at the help of update command for more informations.'''
    def test(ui, repo, node=None, rev=None, date=None, check=False):
        if rev and node:
            raise util.Abort(_("please specify just one revision"))

        if not rev:
            rev = node

        if check:
            c = repo[None]
            if c.modified() or c.added() or c.removed():
                raise util.Abort(_("uncommitted local changes"))

        if date:
            rev = cmdutil.finddate(ui, repo, date)
    _nested_apply(ui, repo, test, False, node=node, rev=rev, date=date,
            check=check)
    _nested_apply(ui, repo, commands.update, True, node=node, rev=rev,
            clean=clean, date=date, check=check)
