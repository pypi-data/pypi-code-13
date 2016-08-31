"""Test kit for utilities package.

   Some of these are going to seem pretty silly, as the utils are largely
   convenience methods.
"""

from webapptitude import testkit as helper
from webapptitude import util

from unittest import expectedFailure


class UtilitiesTest(helper.TestCase):
    stubs = False  # stubs are not needed for this group of tests

    @expectedFailure
    def testThisTestWillFail(self):
        self.assertTrue(False)

    def testMD5Checksum(self):
        checksum = util.md5("hello")
        self.assertEqual(checksum, "5d41402abc4b2a76b9719d911017c592")

    def testDevelEnviron(self):
        self.assertEqual(util.is_dev_server(), True)

    # @helper.debug_on(TypeError)
    def testExpirationTime(self):
        target = util.datetime8601.tzaware(util.datetime.utcnow(), util.UTC())
        result = util.expires_time_parse(util.expires_time(10))
        self.assertEqual(target + util.timedelta(seconds=10), result)

    def testEmailDomainCheck(self):
        self.assertTrue(util.user_in_domain('sam@example.com', 'example.com'))
        self.assertFalse(util.user_in_domain('sam@example.com', 'pizza.com'))

    def testDictionaryExplorers(self):
        context = util.odict(test=True, pizza="yummy", pref={'two': 7},
                             q=[{'test': 'yes'}])
        self.assertTrue(context.get('test'))
        self.assertEqual(context.get('pizza'), 'yummy')
        self.assertEqual(context.pref.two, 7)
        self.assertEqual(context.q[0].test, 'yes')

    def testBase62Encoding(self):
        value = 201739183
        self.assertEqual(value, util.base62decode(util.base62encode(value)))

    def testRandomTimeCode(self):
        result = util.generate_unique_timecode()
        self.assertTrue(result)