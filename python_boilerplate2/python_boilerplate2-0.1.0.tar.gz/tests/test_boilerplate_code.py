from python_boilerplate.python_boilerplate import Cal


def test_cal():
    calc = Cal()

    assert calc.jog(2, 3) == 5
    assert calc.jog(3, -3) == 0
    assert calc.biyog(3, -3) == 6
    assert calc.biyog(3, 3) == 0
