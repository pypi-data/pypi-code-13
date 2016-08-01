import errno
import os
import shutil
import subprocess
import tempfile


from bzrlib import osutils


def override_env_var(name, value):
    """Modify the environment, setting or removing the env_variable.

    :param name: The environment variable to set.

    :param value: The value to set the environment to. If None, then
        the variable will be removed.

    :return: The original value of the environment variable.
    """
    orig = os.environ.get(name)
    if value is None:
        if orig is not None:
            del os.environ[name]
    else:
        # FIXME: supporting unicode values requires a way to acquire the
        # user encoding, punting for now -- vila 2013-01-30
        os.environ[name] = value
    return orig


def override_env(test, name, new):
    """Set an environment variable, and reset it after the test.

    :param name: The environment variable name.

    :param new: The value to set the variable to. If None, the variable is
        deleted from the environment.

    :returns: The actual variable value.
    """
    value = override_env_var(name, new)
    test.addCleanup(override_env_var, name, value)
    return value


isolated_environ = {
    'HOME': None,
}


def isolate_env(test, env=None):
    """Isolate test from the environment variables.

    This is usually called in setUp for tests that needs to modify the
    environment variables and restore them after the test is run.

    :param test: A test instance

    :param env: A dict containing variable definitions to be installed. Only
        the variables present there are protected. They are initialized with
        the provided values.
    """
    if env is None:
        env = isolated_environ
    for name, value in env.items():
        override_env(test, name, value)


def set_cwd_to_tmp(test):
    """Create a temp dir an cd into it for the test duration.

    This is generally called during a test setup.
    """
    test.test_base_dir = tempfile.mkdtemp(prefix='mytests-', suffix='.tmp')
    test.addCleanup(shutil.rmtree, test.test_base_dir, True)
    current_dir = os.getcwdu()
    test.addCleanup(os.chdir, current_dir)
    os.chdir(test.test_base_dir)


# FIXME: Borrowed from bzrlib, needs a better home -- vila 2013-08-05
class Feature(object):
    """An operating system Feature."""

    def __init__(self):
        self._available = None

    def available(self):
        """Is the feature available?

        :return: True if the feature is available.
        """
        if self._available is None:
            self._available = self._probe()
        return self._available

    def _probe(self):
        """Implement this method in concrete features.

        :return: True if the feature is available.
        """
        raise NotImplementedError

    def __str__(self):
        if getattr(self, 'feature_name', None):
            return self.feature_name()
        return self.__class__.__name__


class ExecutableFeature(Feature):
    """Feature testing whether an executable of a given name is on the PATH."""

    def __init__(self, name):
        super(ExecutableFeature, self).__init__()
        self.name = name
        self._path = None

    @property
    def path(self):
        # This is a property, so accessing path ensures _probe was called
        self.available()
        return self._path

    def _probe(self):
        self._path = osutils.find_executable_on_path(self.name)
        return self._path is not None

    def feature_name(self):
        return '%s executable' % self.name


qemu_img_feature = ExecutableFeature('qemu-img')


class _UseSudoForTestsFeature(Feature):
    """User has sudo access.

    There is no direct way to test for sudo access other than trying to use
    it. This is not something we can do in automated tests as it requires user
    input.

    Whatever trick is used to guess whether or not the user *can* sudo won't
    tell us if she agrees to run the sudo tests. Instead, this should rely on
    an opt-in mechanism so each user decides whether or not she wants to run
    the tests.
    """

    def _probe(self):
        # I.e. if you want to run the tests that requires sudo issue:
        # $ touch ~/.setup_vm.use_sudo_for_tests
        # if you don't, issue:
        # $ rm -f ~/.setup_vm.use_sudo_for_tests
        path = os.path.expanduser('~/.setup_vm.use_sudo_for_tests')
        return os.path.exists(path)

    def feature_name(self):
        return 'sudo access'


use_sudo_for_tests_feature = _UseSudoForTestsFeature()


class _SshFeature(ExecutableFeature):

    def __init__(self):
        super(_SshFeature, self).__init__('ssh')
        self.version = None

    def _probe(self):
        exists = super(_SshFeature, self)._probe()
        if exists:
            try:
                proc = subprocess.Popen(['ssh', '-V'],
                                        stderr=subprocess.PIPE,
                                        stdout=subprocess.PIPE)
                out, err = proc.communicate()
            except OSError as e:
                if e.errno == errno.ENOENT:
                    # broken install
                    return False
                else:
                    raise
            self.version = err
        return exists

    def requires_ecdsa(self, test):
        ecdsa_support = 'OpenSSH_5.9p1-5ubuntu.1.1'
        if self.version < ecdsa_support:
            test.skip('ecdsa requires ssh >= %s, you have %s'
                      % (ecdsa_support, self.version,))


ssh_feature = _SshFeature()


def requires_feature(test, feature):
    if not feature.available():
        test.skip('%s is not available' % feature.feature_name())
