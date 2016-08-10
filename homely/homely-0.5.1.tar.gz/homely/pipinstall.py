import os
import subprocess

from click import echo

from homely._errors import HelperError
from homely.general import UpdateHelperOld
from homely._ui import verbecho
from homely._engine import getengine


def pipinstall(packagename, which="ANY", user=True):
    assert which in (2, 3, "ANY")
    helper = PIPInstall(packagename, which, user)
    getengine().add(helper)


class PIPInstall(UpdateHelperOld):
    _name = None
    _which = None
    _user = False

    def __init__(self, name, which, user):
        super(PIPInstall, self).__init__()
        self._name = name
        self._which = which
        self._user = user
        self._pipcmd = {2: "pip2", 3: "pip3", "ANY": "pip"}[which]

    @property
    def identifiers(self):
        return dict(name=self._name, which=self._which)

    @classmethod
    def fromidentifiers(class_, identifiers):
        return class_(identifiers["name"], identifiers["which"], True)

    def iscleanable(self):
        return self._isinstalled()

    def isdone(self):
        # ask pip if the package is installed or not
        return self._isinstalled()

    def _isinstalled(self):
        cmd = [self._pipcmd, 'show', self._name]
        import pprint
        print('cmd = ' + pprint.pformat(cmd))  # noqa TODO
        with open(os.devnull, 'w') as devnull:
            return 0 == subprocess.call(cmd)
            return 0 == subprocess.call(cmd, stdout=devnull, stderr=devnull)

    def descchanges(self):
        return 'pip install: %s install %s%s' % (
            self._pipcmd,
            self._name,
            ' --user' if self._user else '',
        )

    def makechanges(self):
        raise Exception("TODO: pip install the thing")  # noqa
        changes = {}
        return changes

    def undochanges(self, changes):
        raise Exception("TODO: do we want to uninstall the package?")  # noqa


class InstallFromSource(UpdateHelperOld):
    _title = None
    _source_repo = None
    _clone_to = None
    _real_clone_to = None
    _branch = None
    _tag = None
    _symlinks = []
    _compile = None

    def __init__(self, source_repo, clone_to):
        super(InstallFromSource, self).__init__()
        self._title = 'Install %s into %s' % (source_repo, clone_to)
        self._source_repo = source_repo
        self._clone_to = clone_to
        self._real_clone_to = os.path.expanduser(clone_to)

    @property
    def identifiers(self):
        return dict(source_repo=self._source_repo,
                    clone_to=self._clone_to)

    @classmethod
    def fromidentifiers(class_, identifiers):
        return class_(identifiers["source_repo"], identifiers["clone_to"])

    def select_branch(self, branch_name):
        assert self._tag is None
        self._branch = branch_name

    def select_tag(self, tag_name):
        assert self._branch is None
        self._tag = tag_name

    def symlink(self, source, dest):
        self._symlinks.append((os.path.join(self._real_clone_to, source),
                               os.path.expanduser(dest)))

    def compile_cmd(self, commands):
        assert self._compile is None
        self._compile = commands

    def iscleanable(self):
        return os.path.exists(self._real_clone_to)

    def isdone(self):
        if not os.path.exists(self._real_clone_to):
            return False

        # if a branch is requested, then we always need to check again ...
        if self._branch is not None:
            return False

        # has the correct branch or tag been checked out?
        assert self._tag is not None
        current = subprocess.check_output(
            ['git', 'tag', '--points-at', 'HEAD'],
            cwd=self._real_clone_to)
        if self._tag not in map(str, current.splitlines()):
            return False

        # do the symlinks exist?
        for source, dest in self._symlinks:
            # FIXME: return not-done if the target files don't exist
            if not os.path.islink(dest):
                return False

        # FIXME: it is possible that the compilation step may have failed, and
        # we have no way to determine if that is the case.

        # it appears to be done ... yay
        return True

    def descchanges(self):
        return self._title

    def makechanges(self, prevchanges):
        assert self._source_repo is not None
        assert self._clone_to is not None
        changes = {}
        if not os.path.exists(self._real_clone_to):
            echo("Cloning %s" % self._source_repo)
            pull_needed = False
            cmd = ['git', 'clone', self._source_repo, self._real_clone_to]
            subprocess.run(cmd)
            changes["made_clone_dir"] = True
        else:
            echo("Updating %s from %s" % (self._clone_to, self._source_repo))
            pull_needed = True
            if not os.path.exists(os.path.join(self._real_clone_to, '.git')):
                raise HelperError("%s is not a git repo" % self._real_clone_to)
            changes["made_clone_dir"] = prevchanges.get("made_clone_dir",
                                                        False)

        # do we want a particular branch?
        if self._branch:
            subprocess.run(['git', 'checkout', self._branch],
                           cwd=self._real_clone_to)
            if pull_needed:
                subprocess.run(['git', 'pull'], cwd=self._real_clone_to)
        else:
            assert self._tag is not None
            if pull_needed:
                subprocess.run(['git', 'fetch', '--tags'],
                               cwd=self._real_clone_to)
            subprocess.run(['git', 'checkout', self._tag],
                           cwd=self._real_clone_to)

        # run any compilation commands
        if self._compile is not None:
            # FIXME: we probably need to delete all the symlink targets before
            # compiling, as this is our best way of determining that the
            # compilation has failed ...
            for cmd in self._compile:
                subprocess.run(cmd, cwd=self._real_clone_to)

        # what symlinks were created last time? What symlinks need to be
        # created now?
        newsymlinks = set([dest for _, dest in self._symlinks])
        for path in prevchanges.get("symlinks_made", []):
            if os.path.islink(path) and path not in newsymlinks:
                verbecho("Cleaning up symlink: %s" % path)
                os.unlink(path)

        # create new symlinks
        changes["symlinks_made"] = []
        for source, dest in self._symlinks:
            verbecho("Ensure symlink exists: %s -> %s" % (source, dest))
            if os.path.islink(dest):
                target = os.readlink(dest)
                if os.path.realpath(target) != os.path.realpath(source):
                    raise HelperError("Symlink %s is not pointing at %s" %
                                      (dest, source))
                continue
            if os.path.exists(dest):
                raise HelperError("%s already exists" % dest)
            os.symlink(source, dest)
            changes["symlinks_made"].append(dest)

        return changes

    def undochanges(self, prevchanges):
        for dest in prevchanges["symlinks_made"]:
            if os.path.islink(dest):
                verbecho("Cleaning up symlink: %s" % dest)
                os.unlink(dest)
