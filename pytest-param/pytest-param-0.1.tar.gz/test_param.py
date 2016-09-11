import pytest

from pytest_param import PYTEST_PARAM_CHOICES


pytest_plugins = "pytester",


@pytest.fixture(params=[
    [None],
    [True, False],
    [1, 2, 3],
])
def params(request):
    """
    List of one, two or three params.
    """
    return request.param


@pytest.fixture(params=[
    """
    import pytest
    @pytest.mark.parametrize('params', %s)
    def test_param(params):
        pass
    """,
    """
    import pytest
    @pytest.fixture(params=%s)
    def fixture(request):
        return request.param
    def test_param(fixture):
        pass
    """,
])
def pyfile(request, params):
    """
    Python source for `test_param` with marked parameters or with a
    fixture that has marked parameters.
    """
    return request.param % params


@pytest.mark.parametrize('choice', PYTEST_PARAM_CHOICES)
def test_no_param(testdir, choice):
    """
    A test without parameters should run regardless of the param option.
    """
    testdir.makepyfile("""
        def test_no_param():
            pass
    """)
    result = testdir.runpytest('-v', '--param=%s' % choice)
    result.stdout.fnmatch_lines([
        '*test_no_param.py::test_no_param*',
        '*1 passed*',
    ])


@pytest.mark.parametrize('choice', PYTEST_PARAM_CHOICES)
def test_one_param(testdir, choice):
    """
    A test with one parameter should run regardless of the param option.
    """
    testdir.makepyfile("""
        import pytest
        @pytest.mark.parametrize('param', [True])
        def test_one_param(param):
            pass
    """)
    result = testdir.runpytest('-v', '--param=%s' % choice)
    result.stdout.fnmatch_lines([
        '*test_one_param.py::test_one_param[[]True[]]*',
        '*1 passed*',
    ])


def test_all_param(testdir, pyfile, params):
    """
    The `all` param should run a test for all parameters.
    """
    testdir.makepyfile(pyfile)
    result = testdir.runpytest('-v', '--param=all')
    result.stdout.fnmatch_lines([
        '*test_all_param.py::test_param[[]%s[]]*' % param
        for param in params
    ] + [
        '*%d passed*' % len(params),
    ])


def test_first_param(testdir, pyfile, params):
    """
    The `first` param should run a test for the first parameter.
    """
    testdir.makepyfile(pyfile)
    result = testdir.runpytest('-v', '--param=first')
    result.stdout.fnmatch_lines([
        '*test_first_param.py::test_param[[]%s[]]*' % params[0],
        '*1 passed*',
    ])


def test_last_param(testdir, pyfile, params):
    """
    The `last` param should run a test for the last parameter.
    """
    testdir.makepyfile(pyfile)
    result = testdir.runpytest('-v', '--param=last')
    result.stdout.fnmatch_lines([
        '*test_last_param.py::test_param[[]%s[]]*' % params[-1],
        '*1 passed*',
    ])


def test_random_param(testdir, pyfile, params):
    """
    The `random` param should run a test for a random parameter.
    """
    testdir.makepyfile(pyfile)
    result = testdir.runpytest('-v', '--param=random')
    result.stdout.fnmatch_lines([
        '*test_random_param.py::test_param*',
        '*1 passed*',
    ])
