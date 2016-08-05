'''
Created on Apr 28, 2016

@author: iitow
'''
from pluginable import Plugin
from modules.git_kit import Branch_actions, Repo_actions, Commit_actions
from modules.terminal import shell
from modules.log import message

class git(Plugin):
    ''' This class Represents a call to git
    '''
    def __init__(self, action_manager):
        '''
        git Constructor

        :param action_manager: Obj, from action_manager class
        '''
        self.action_manager = action_manager
        Plugin.__init__(self, self.action_manager)
    
    def latest_commit(self, user, local_path, branch, info_type, **defaults):
        '''
        get the latest commit info from a branch
        :param user: String, username
        :param local_path: String, full path and desired dir name
        :param branch: String
        :param info_type: String, sha1, message, author
        :return: String
        :example:
        ```
                - scm.git.latest_commit:
                      - "root"
                      - "/tmp/goephor"
                      - "refactor"
                      - "sha1"
        ```
        '''
        repo = Repo_actions(local_path, user=user)
        branch_obj = Branch_actions(repo)
        commit_obj = Commit_actions(repo)
        branch_is = branch_obj.checkout(branch)
        if not branch_is:
            raise Exception('Unable to checkout %s' % branch)
        latest = commit_obj.latest()
        latest = latest.get(info_type,None)
        if self.verbose:
            print message('info',"[latest_commit] %s is %s" % (info_type,latest),debug=self.debug)
        return latest

    def clone(self,
              user,
              new_local_path,
              remote,
              **defaults):
        '''
        Clone a git repo

        :param user: String, username
        :param new_local_path: String, full path and desired dir name
        :param remote: String, git repo
        :param branch: define the branch to checkout
        :param depth: to perform a shallow clone
        :example:
        ```
               - scm.git.clone:
                      - "root"
                      - "/tmp/goephor"
                      - "git@github.west.isilon.com:eng-tools/goephor"
        ```
        '''
        print message('info',"[clone] @ %s -> %s" % (remote, new_local_path),debug=self.debug)
        for key, value in defaults.iteritems():
            print message('info',"%s=%s" % (key, value),debug=self.debug)
        print ""
        repo = Repo_actions(new_local_path, user=user)
        if not defaults.get('branch'):
            defaults['branch']='master'
        has_cloned = repo.clone(remote,**defaults)
        if has_cloned:
            return True
        else:
            raise Exception('Unable to Clone %s' % remote)

    def checkout(self, user, local_path, branch):
        '''
        checkout a local branch
        :param user: String, username
        :param local_path: String, full path and desired dir name
        :param branch: String
        ```
                - scm.git.checkout:
                      - "root"
                      - "/tmp/goephor"
                      - "refactor"
        ```
        '''
        repo = Repo_actions(local_path, user=user)
        branch_obj = Branch_actions(repo)
        branch_is = branch_obj.checkout(branch)
        if not branch_is:
            raise Exception('Unable to checkout %s' % branch)
        return branch_is

    def delete(self, local_path, **defaults):
        '''
        Delete a local repo
        :param local_path: String
        :example:
        ```
            - scm.git.delete:
                - "/tmp/goephor"
        ```
        '''
        repo = Repo_actions(local_path)
        has_attached = repo.attach(local_path)
        if has_attached:
            session = shell("rm -rf %s" % (local_path))
            if session.get('code') == 0:
                return True
        else:
            print message('info',"[Pass] not a repo @ %s " % (local_path),debug=self.debug)
