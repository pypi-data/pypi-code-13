# -*- coding: utf-8 -*-
# Copyright (c) 2016 Felix Krull <f_krull@gmx.de>
# Released under the terms of the BSD license; see LICENSE.

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import colorhash


def data_driven_test(cls):
    for i, (input, output) in enumerate(cls.data):
        def test(self):
            self.assertEqual(self.transform(input), output)
        test.__doc__ = '%r -> %r' % (input, output)
        setattr(cls, 'test_%s' % i, test)
    return cls


@data_driven_test
class TestHsl2Rgb(unittest.TestCase):
    data = [
        ((0, 1, 0.5), (255, 0, 0)),
        ((120, 1, 0.75), (128, 255, 128)),
        ((240, 1, 0.25), (0, 0, 128)),
        ((330, 1, 0.75), (255, 128, 191)),
        ((49.5, 0.893, 0.497), (240, 200, 14))
    ]

    def transform(self, x):
        return colorhash.hsl2rgb(x)

    def test_not_iterable(self):
        with self.assertRaises(ValueError):
            colorhash.hsl2rgb(45)

    def test_not_enough_elems(self):
        with self.assertRaises(ValueError):
            colorhash.hsl2rgb([1, 0.5])

    def test_too_many_elems(self):
        with self.assertRaises(ValueError):
            colorhash.hsl2rgb([1, 0.5, 1, 1])

    def test_h_not_number(self):
        with self.assertRaises(ValueError):
            colorhash.hsl2rgb(['100', 0, 1])

    def test_s_not_number(self):
        with self.assertRaises(ValueError):
            colorhash.hsl2rgb([100, '0', 1])

    def test_l_not_number(self):
        with self.assertRaises(ValueError):
            colorhash.hsl2rgb([100, 0, '1'])


@data_driven_test
class TestRgb2Hex(unittest.TestCase):
    data = [
        ((0, 0, 0), '#000000'),
        ((255, 255, 255), '#ffffff'),
        ((0, 0, 237), '#0000ed'),
        ((255, 64, 0), '#ff4000'),
        ((1, 15, 16), '#010f10'),
    ]

    def transform(self, x):
        return colorhash.rgb2hex(x)

    def test_not_iterable(self):
        with self.assertRaises(ValueError):
            colorhash.rgb2hex(45)

    def test_not_enough_elems(self):
        with self.assertRaises(ValueError):
            colorhash.rgb2hex([1, 255])

    def test_too_many_elems(self):
        with self.assertRaises(ValueError):
            colorhash.rgb2hex([255, 255, 255, 1])

    def test_r_not_number(self):
        with self.assertRaises(ValueError):
            colorhash.rgb2hex(['100', 0, 1])

    def test_g_not_number(self):
        with self.assertRaises(ValueError):
            colorhash.rgb2hex([100, '0', 1])

    def test_b_not_number(self):
        with self.assertRaises(ValueError):
            colorhash.rgb2hex([100, 0, '1'])


def custom_hash(s):
    return sum(ord(c) for c in s)


class TestColorHash_Lightness_Saturation(unittest.TestCase):
    def test_defaults(self):
        c = colorhash.ColorHash('')
        self.assertEqual(c.hsl[1:], (0.35, 0.35))

    def test_lightness_saturation_values(self):
        c = colorhash.ColorHash('', lightness=0.5, saturation=0.5)
        self.assertEqual(c.hsl[1:], (0.5, 0.5))

    def test_lightness_saturation_arrays(self):
        c = colorhash.ColorHash('', lightness=[0.9, 1], saturation=[0.9, 1])
        self.assertEqual(c.hsl[1:], (0.9, 0.9))


class TestColorHash_CustomHash(unittest.TestCase):
    hsl = (custom_hash('abc') % 359, 0.35, 0.35)
    rgb = colorhash.hsl2rgb(hsl)
    hex = colorhash.rgb2hex(rgb)

    def test_hsl(self):
        self.assertEqual(
            colorhash.ColorHash('abc', hashfunc=custom_hash).hsl,
            self.hsl)

    def test_rgb(self):
        self.assertEqual(
            colorhash.ColorHash('abc', hashfunc=custom_hash).rgb,
            self.rgb)

    def test_hex(self):
        self.assertEqual(
            colorhash.ColorHash('abc', hashfunc=custom_hash).hex,
            self.hex)


if __name__ == '__main__':
    unittest.main()
