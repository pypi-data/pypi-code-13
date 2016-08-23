import pytest

#all pass
#pass + skip
#all skip
#pass + error
#all errors
#pass + exception
#all exceptions
#pass + skip + exceptions + error

pytest_plugins = "pytester"


def test_all_pass(testdir):
    testdir.makepyfile(
        """
        def test_selenium_3plus3():
            assert 3+3 == 6

        def test_selenium_1plus1():
            assert 1+1 == 2
        """
    )
    result = testdir.runpytest("--verbose")
    result.assert_outcomes(passed=2)


def test_pass_skip(testdir):
    testdir.makepyfile(
        """
        import pytest

        def test_selenium_3plus3():
            assert 3+3 == 6

        @pytest.mark.skip()
        def test_selenium_1plus1():
            assert 1+1 == 2
        """
    )
    result = testdir.runpytest("--verbose")
    result.assert_outcomes(passed=1, skipped=1)
