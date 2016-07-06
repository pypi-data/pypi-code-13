from amo2kinto.compare import MAXVERSION, version_int, version_dict


def test_version_int():
    """Tests that version_int. Corrects our versions."""
    assert version_int('3.5.0a1pre2') == 3050000001002
    assert version_int('') == 200100
    assert version_int('0') == 200100
    assert version_int('*') == 99000000200100
    assert version_int(MAXVERSION) == MAXVERSION
    assert version_int(MAXVERSION + 1) == MAXVERSION
    assert version_int('9999999') == MAXVERSION


def test_version_int_compare():
    assert version_int('3.6.*') == version_int('3.6.99')
    assert version_int('3.6.*') > version_int('3.6.8')


def test_version_asterix_compare():
    assert version_int('*') == version_int('99')
    assert version_int('98.*') < version_int('*')
    assert version_int('5.*') == version_int('5.99')
    assert version_int('5.*') > version_int('5.0.*')


def test_version_dict():
    assert version_dict('5.0') == (
        {'major': 5,
         'minor1': 0,
         'minor2': None,
         'minor3': None,
         'alpha': None,
         'alpha_ver': None,
         'pre': None,
         'pre_ver': None})


def test_version_int_unicode():
    assert version_int(u'\u2322 ugh stephend') == 200100
