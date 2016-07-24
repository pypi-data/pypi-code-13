import unittest
import hark_builder.build


class TestBuild(unittest.TestCase):
    def test_build_str(self):
        b = hark_builder.build.Build('Debian-7_Virtualbox')
        assert str(b) == 'Debian-7 - Virtualbox'

    def test_all(self):
        a = hark_builder.build.Build.all()
        assert len(a) == 3

    def test_by_name(self):
        name = 'Debian-7_Virtualbox'
        b = hark_builder.build.Build.by_name(name)
        assert b.name == name
