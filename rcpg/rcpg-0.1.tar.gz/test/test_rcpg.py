import unittest
import rcpg

class ChordMapTestCase(unittest.TestCase):
    def setUp(self):
        self.cm = rcpg.ChordMap()
        self.c = (50,54,57)
        self.d = (52,56,59)
        self.e = (49,54,57)
        self.f = (50,55,59)
        self.g = (49,52,57)
        self.a = (50,54,59)
        self.b = (49,52,55)

class ChordValidityTestCase(ChordMapTestCase):
    def testKeyChordAsListRaisesChordError(self):
        self.assertRaises(rcpg.ChordError, self.cm.addChord, list(self.c), ((5,self.f),(4,self.g),(1,self.a)))
    def testNegativeNoteInKeyRaisesChordError(self):
        self.assertRaises(rcpg.ChordError, self.cm.addChord, (50,-3,59), ((5,self.f),(4,self.g),(1,self.a)))
    def testNoteTooHighInKeyRaisesChordError(self):
        self.assertRaises(rcpg.ChordError, self.cm.addChord, (50,130,59), ((5,self.f),(4,self.g),(1,self.a)))
    def testFloatNoteInKeyRaisesChordError(self):
        self.assertRaises(rcpg.ChordError, self.cm.addChord, (50,13.1,59), ((5,self.f),(4,self.g),(1,self.a)))
    def testNonNumberNoteInKeyRaisesChordError(self):
        self.assertRaises(rcpg.ChordError, self.cm.addChord, (50,'foo',59), ((5,self.f),(4,self.g),(1,self.a)))
    def testValueContainsChordAsListRaisesChordError(self):
        self.assertRaises(rcpg.ChordError, self.cm.addChord, self.c, ((5,self.f),(4,list(self.g)),(1,self.a)))
    def testNegativeNoteInValueRaisesChordError(self):
        self.assertRaises(rcpg.ChordError, self.cm.addChord, self.c, ((5,(50,-3,61)),(4,self.g),(1,self.a)))
    def testNoteTooHighInValueRaisesChordError(self):
        self.assertRaises(rcpg.ChordError, self.cm.addChord, self.c, ((5,(50,130,61)),(4,self.g),(1,self.a)))
    def testFloatNoteInValueRaisesChordError(self):
        self.assertRaises(rcpg.ChordError, self.cm.addChord, self.c, ((5,(50,13.1,61)),(4,self.g),(1,self.a)))
    def testNonNumberNoteInValueRaisesChordError(self):
        self.assertRaises(rcpg.ChordError, self.cm.addChord, self.c, ((5,(50,'foo',61)),(4,self.g),(1,self.a)))
    def testWeightAsFloatRaisesChordWeightError(self):
        self.assertRaises(rcpg.ChordWeightError, self.cm.addChord, self.c, ((5.5,self.f),(4,self.g),(1,self.a)))
    def testNegativeWeightRaisesChordWeightError(self):
        self.assertRaises(rcpg.ChordWeightError, self.cm.addChord, self.c, ((-5,self.f),(4,self.g),(1,self.a)))
    def testMissingWeightRaisesChordWeightError(self):
        self.assertRaises(rcpg.ChordWeightError, self.cm.addChord, self.c, ((self.f,),(4,self.g),(1,self.a)))
        self.assertRaises(rcpg.ChordWeightError, self.cm.addChord, self.c, (self.f,(4,self.g),(1,self.a)))
    def testEverythingValidRaisesNoErrors(self):
        try:
            self.cm.addChord(self.c,((5,self.f),(4,self.g),(1,self.a)))
        except rcpg.ChordError:
            self.fail()

class GenerateProgressionTestCase(ChordMapTestCase):
    def setUp(self):
        ChordMapTestCase.setUp(self)
        self.cm.addChord(self.a,((2,self.f),(3,self.g),(1,self.e),(1,self.b),(2,self.c),(1,self.d)))
        self.cm.addChord(self.b,((4,self.c),(4,self.a),(2,self.d)))
        self.cm.addChord(self.c,((3,self.f),(2,self.g),(2,self.d),(1,self.e),(1,self.b),(1,self.a)))
        self.cm.addChord(self.d,((1,self.f),(4,self.g),(3,self.e),(1,self.b),(1,self.a)))
        self.cm.addChord(self.e,((3,self.f),(1,self.g),(6,self.a)))
        self.cm.addChord(self.f,((3,self.c),(2,self.g),(2,self.d),(1,self.e),(1,self.b),(1,self.a)))
    def testIncompleteChordMapRaisesChordMapError(self):
        re = r"These chords are mapped to but not mapped from:\[\(49, 52, 57\)\]"
        self.assertRaisesRegexp(rcpg.ChordMapError, re, self.cm.generateProgression, 10, self.c)
    def testInvalidStartChordRaisesChordError(self):
        self.cm.addChord(self.g,((1,self.f),(1,self.c),(1,self.d),(2,self.e),(2,self.b),(3,self.a)))
        self.assertRaises(rcpg.ChordError, self.cm.generateProgression, 10, (50, -1, 59))
    def testInvalidLengthValueRaisesValueError(self):
        self.cm.addChord(self.g,((1,self.f),(1,self.c),(1,self.d),(2,self.e),(2,self.b),(3,self.a)))
        self.assertRaises(ValueError, self.cm.generateProgression, -5, self.c)
        self.assertRaises(ValueError, self.cm.generateProgression, 0, self.c)
    def testLengthAsFloatRaisesTypeError(self):
        self.cm.addChord(self.g,((1,self.f),(1,self.c),(1,self.d),(2,self.e),(2,self.b),(3,self.a)))
        self.assertRaises(TypeError, self.cm.generateProgression, 10.5, self.c)
    def testEverythingValidRaisesNoErrors(self):
        self.cm.addChord(self.g,((1,self.f),(1,self.c),(1,self.d),(2,self.e),(2,self.b),(3,self.a)))
        try:
            prog = self.cm.generateProgression(10, self.c)
            self.assertIsInstance(prog, list)
            self.assertTrue(len(prog) > 0)
            for c in prog:
                self.assertIsInstance(c, tuple)
        except rcpg.ChordMapError:
            self.fail()

