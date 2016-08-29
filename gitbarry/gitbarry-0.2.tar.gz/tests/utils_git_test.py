from unittest import TestCase
from gitbarry.utils import git

class UtilsGitTests(TestCase):
    def test_assert_is_git_repo(self):
        git.assert_is_git_repo()
