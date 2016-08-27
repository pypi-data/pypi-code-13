
import unittest

from yaoguang.entity import Entity


class Test(unittest.TestCase):

    def testEntity(self):

        e = Entity({"int": 1, "string": "hello", "map": {"int": 2}})
        print(repr(e))

        self.assertEquals(1, e.int)
        self.assertEquals("hello", e.string)
        self.assertEquals({"int":2}, e.map)
        self.assertEquals('{"int": 1, "map": {"int": 2}, "string": "hello"}', e.as_json())
        self.assertEquals({"int":3}, e.map)



if __name__ == '__main__':
    unittest.main()
