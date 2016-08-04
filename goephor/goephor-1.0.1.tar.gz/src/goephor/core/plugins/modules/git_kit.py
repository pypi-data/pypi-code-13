'''
Created on Oct 8, 2015

:author: iitow
'''
import os
import sys
from git import Repo
from terminal import shell


class Repo_actions(object):
    def __init__(self,
                 repo_path,
                 set_bare=False,
                 user='root',
                 git_host='github.west.isilon.com',
                 set_ssh_config=True):
        """
        Initialize Repo actions
        """
        self.ssh_config = '/%s/.ssh/config' % (user)
        self.repo_path = repo_path
        self.repo = None
        self.is_attached = self.attach(self.repo_path)
        if set_ssh_config:
            self._set_ssh_config(self.ssh_config, git_host)

    def _set_ssh_config(self,
                        ssh_config,
                        git_host):
        """
        This turns off host verification

        :param ssh_config: path to <user>/.ssh/config
        :param git_host: example. github.west.isilon.com
        """
        if os.path.exists(ssh_config):
            with open(ssh_config, 'r') as file:
                config = file.read()
                if git_host not in config:
                    print "[Info] adding host @ %s" % (ssh_config)
                    cmd = ("sudo printf "
                           "'Host %s\\n\\tStrictHostKeyChecking no\\n' "
                           ">> %s") % (git_host, ssh_config)
                    shell(cmd, shell=True)
        else:
            print "[Info] Creating ssh config @ %s" % (ssh_config)
            cmd = ("sudo printf "
                   "'Host %s\\n\\tStrictHostKeyChecking no\\n' "
                   "> %s") % (git_host, ssh_config)
            shell(cmd, shell=True)

    def _set_dirs(self, strict=True):
        if not os.path.isdir(self.repo_path):
            os.makedirs(self.repo_path)
            print "[Create Directories] %s" % self.repo_path
        if os.path.isdir(self.repo_path):
            return True
        print "[Error] Unable to create dir %" % self.repo_path
        if strict:
            sys.exit(1)
        return False

    def attach(self,
               repo_path):
        """
        attach to a git repo on your local system

        :param repo_path: system path to repo
        :return: boolean, success/failure
        """
        try:
            repo = Repo(repo_path)
            print "[Repo Attach] @ %s" % repo_path
            self.repo = repo
            return True
        except Exception:
            print "[Info] not a repo %s" % repo_path
            self.repo = None
        return False

    def _initial_commit(self):
        """
        To fully init an empty rep
        """
        if not self.repo:
            print "[Warning] not attached to a repo"
            return False
        readme = 'README.md'
        readme_path = '%s/%s' % (self.repo_path, readme)
        try:
            with open(readme_path, 'w') as file:
                file.write('\n')
            if not os.path.exists(readme_path):
                print '[Warning] README.md not found'
                return False
            self.add(readme)
            self.commit('initial commit')
        except Exception as e:
            print e
        return False

    def init(self,
             set_bare=False):
        """
        Initialize a new repo on your local system

        :param set_bare: boolean, default is False, creates a 'bare repo',
        to run like a src repo
        :return: boolean, success/failure
        :note: Shared repositories should always be created with the set_bare
        flag and should be stored in a directory called <projectname>.git
        """
        self._set_dirs()
        try:
            repo = Repo(self.repo_path)
            self.repo = repo
            print "[Active Repo] @ %s" % (self.repo_path)
            return True
        except Exception:
            repo = Repo.init(self.repo_path, bare=set_bare)
            self.repo = repo
            self._initial_commit()
            print '[init] %s' % self.repo_path
            return True
        return False

    def clone(self,
              remote_ssh,
              **defaults):
        """
        Clone a repository from a remote location

        :param remote_ssh: provide the ssh full info
        example. git@github.west.isilon.com:iitow/scm-tools.git
        :return: boolean, success/failure
        """
        try:
            print "[Clone] @ %s" % self.repo_path
            repo = Repo.clone_from(remote_ssh,
                                    self.repo_path,
                                    **defaults)
            self.repo = repo
            return True
        except Exception as e:
            if 'already exists' in str(e):
                return True
            else:
                print e
        return False

    def untracked_files(self):
        """
        list all untracked files

        :return: list of untracked files
        """
        if not self.repo:
            print "[Warning] not attached to a repo"
            return []
        return self.repo.untracked_files


class Commit_actions(object):
    """ This class handles all commit type actions
    """
    def __init__(self, repo):
        self.repo = repo.repo

    def commit(self,
               msg):
        """
        Commits changes

        :param msg: string, the commit message
        :return: boolean, success/failure
        """
        if not self.repo:
            print "[Warning] not attached to a repo"
            return False
        try:
            self.repo.index.commit(msg)
            return True
        except Exception as e:
            print e
        return False

    def cherry_pick(self,
                    sha1_str,
                    merge=False):
        """
        Cherry picks a commit

        :param sha1_str: sha1 string of commit
        :return: boolean True/False
        """
        if not self.repo:
            print "[Warning] not attached to a repo"
            return False
        try:
            if merge:
                self.repo.git.cherry_pick(sha1_str, '-x', '-m')
            else:
                self.repo.git.cherry_pick(sha1_str, '-x')
            return True
        except Exception as e:
            print e
        return False

    def diff_tree(self,
                  sha1_str):
        '''
        Performs a diff tree against current and sha1

        :param sha1_str: String
        '''
        if not self.repo:
            print "[Warning] not attached to a repo"
            return False
        try:
            output = self.repo.git.diff_tree('--no-commit-id',
                                             '--name-only',
                                             '-r',
                                             sha1_str)
            return output
        except Exception as e:
            print e
        return None

    def search_log(self,
                   search):
        '''
        Search logs for a given token

        :param search: String token
        '''
        if not self.repo:
            print "[Warning] not attached to a repo"
            return False
        try:
            grep_str = "--grep=%s" % search
            output = self.repo.git.log('--all', grep_str)
            return output
        except Exception as e:
            print e
        return None

    def latest(self):
        if not self.repo:
            print "[Warning] not attached to a repo"
            return False
        try:
            head = self.repo.head.reference
            latest_info = {"sha1":head.commit.hexsha,
                           "message":head.commit.message,
                           "author":head.commit.author.email}
            return latest_info
        except Exception as e:
            print e
        return None
        
        

    def add(self,
            file_name):
        """
        adds files to git index

        :param file_name: name of the file to commit
        :return: boolean, success/failure
        """
        if not self.repo:
            print "[Warning] not attached to a repo"
            return False
        git_dir = self.repo.working_tree_dir
        add_path = '%s/%s' % (git_dir, file_name)
        if not os.path.exists(add_path):
            print "File does not exist %s" % add_path
            return False
        try:
            index = self.repo.index
            index.add([add_path])
            print "[add] %s" % add_path
            return True
        except Exception as e:
            print e
        return False


class Branch_actions(object):
    """
    This class handles all branch related actions

    :requires: Repo obj
    """
    def __init__(self, repo):
        self.repo = repo.repo

    def branch(self,
               branch_name):
        """
        Creates a new local branch

        :param branch_name: string, name of the new branch to create it
        :return: boolean, success/failure
        """
        if not self.repo:
            print "[Warning] not attached to a repo"
            return False
        try:
            self.repo.create_head(branch_name)
            return True
        except Exception as e:
            print e
        return False

    def branch_from(self,
                    src_branch,
                    new_branch):
        """
        Create a branch from existing branch

        :param src_branch: original branch name
        :param dest_branch: new branch name
        """
        if self.checkout(src_branch):
            try:
                self.repo.git.branch(new_branch)
                if self.checkout(new_branch):
                    print "[New Branch] @ %s" % new_branch
                    return True
            except Exception as e:
                print e
        return False

    def branch_is(self):
        """
        provides the current branch

        :return: the current branch
        """
        if not self.repo:
            print "[Warning] not attached to a repo"
            return False
        return self.repo.active_branch

    def branch_list(self,
                    verbose=True):
        """
        provides a list of all branches

        :param verbose: boolean, prints branches out
        :return: list of git.branch objects
        """
        if not self.repo:
            print "[Warning] not attached to a repo"
            return ''
        branches = []
        for branch in self.repo.branches:
            if verbose:
                print branch
            branches.append(branch)
        return branches

    def has_reference(self,
                      branch_name,
                      remote='origin'):
        """
        Search for reference

        :param branch_name: string of branch name
        :return: reference obj
        """
        if not self.repo:
            print "[Warning] not attached to a repo"
            return None
        print "[references]"
        for ref in self.repo.refs:
            name = ref.name
            print name
            if branch_name == name:
                return ref
        return None

    def has_head(self,
                 branch_name):
        """
        Search for branch head

        :param branch_name: string of branch name
        :return: head obj
        """
        if not self.repo:
            print "[Warning] not attached to a repo"
            return None
        for head in self.repo.heads:
            if branch_name == head.name:
                return head
        return None

    def checkout(self,
                 branch_name,
                 remote='origin'):
        """
        checks out a specific branch

        :param branch_name: string, branch you wish to checkout
        :param remote: remote name default is origin
        :return: boolean, success/failure
        """
        if not self.repo:
            print "[Warning] not attached to a repo"
            return False
        reference = self.has_reference(branch_name)
        head = self.has_head(branch_name)
        if head:
            print "[Head Found] @ %s" % head.name
            self.repo.git.checkout(head)
            return True
        elif reference:
            print "[Reference] @ %s" % reference.name
            self.repo.git.checkout(reference, b=branch_name)
            return True
        else:
            print '[Error] Branch %s not found' % (branch_name)
            return False

    def push(self,
             branch_name,
             remote='origin'):
        """
        Push branch to remote

        :param branch_name: string branch name
        :param remote: remote reference
        :return: boolean
        """
        if not self.repo:
            print "[Warning] not attached to a repo"
            return False
        try:
            self.repo.git.push('-u', remote, branch_name)
            return True
        except Exception as e:
            print e
        return False

    def remote_delete(self,
                      branch_name,
                      remote='origin'):
        """
        Deletes branch from github remote

        :param branch_name: string branch name
        :param remote: remote reference
        :return: boolean
        """
        if not self.repo:
            print "[Warning] not attached to a repo"
            return False
        try:
            self.repo.git.push(remote,
                               '--delete',
                               branch_name)
            return True
        except Exception as e:
            print e
        return False

    def delete(self,
               branch_name,
               remote='origin'):
        """
        Delete local branch

        :param branch_name: string branch name
        :param remote: remote reference
        :return: boolean
        """
        if not self.repo:
            print "[Warning] not attached to a repo"
            return False
        try:
            self.checkout('master', remote)
            self.repo.git.branch('-D', branch_name)
            return True
        except Exception as e:
            print e
        return False


class Remote_actions(object):
    """ This class handles all remote actions
    """
    def __init__(self,
                 repo):
        '''
        Remote_actions Constructor
        '''
        self.repo = repo.repo

    def list(self):
        remotes_dict = {}
        remotes = self.repo.git.remote('-v').split('\n')
        for line in remotes:
            if line:
                line = line.split("\t")
                ref = line[0].strip()
                repo = line[1].rsplit(' ', 1)[0].strip()
                remotes_dict[ref] = repo
        return remotes_dict

    def has_remote(self, search):
        remotes = self.list()
        for ref, repo in remotes.iteritems():
            if search in repo:
                return True
        return False

    def add(self,
            remote,
            name='upstream'):
        """
        add a remote to repo

        :param remote: remote url string
        :param name: reference to the remote example. upstream
        :return: boolean True/False
        """
        if not self.repo:
            print "[Warning] not attached to a repo"
            return False
        try:
            self.repo.git.remote('add',
                                 name,
                                 remote)
            return True
        except Exception as e:
            print e
        return False

    def fork_sync(self,
                  remote,
                  name='upstream',
                  branch='master',
                  add_remote=False):
        """
        Syncs a fork of repo with another repository

        :param remote: remote url string
        example. git@github.west.isilon.com:iitow/onefs.git
        :param name: reference to the remote example. upstream
        :return: boolean True/False
        """
        if not self.repo:
            print "[Warning] not attached to a repo"
            return False
        try:
            if add_remote:
                self.add(remote, name)
            self.repo.git.fetch(name)
            self.repo.git.checkout(branch)
            reference = "%s/%s" % (name, branch)
            self.repo.git.merge(reference)
            return True
        except Exception as e:
            print e
        return False

    def fetch(self,
              remote,
              name='upstream',
              branch='master',
              add_remote=False):
        """
        Fetch remote branches

        :param remote: repo url
        example. git@github.west.isilon.com:isilon/onefs.git
        :param name: name of the remote
        :param branch; branch to switch to when fetching
        :param add_remote: boolean add a remote
        :return: boolean
        """
        if not self.repo:
            print "[Warning] not attached to a repo"
            return False
        try:
            if add_remote:
                self.add(remote, name)
            self.repo.git.fetch(name)
            return True
        except Exception as e:
            print e
        return False
