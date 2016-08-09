import random

class ChordError(Exception):
    def __init__(self, chord, message):
        self.chord = chord
        self.message = "%s: %s" % (chord, message)
    def __str__(self):
        return repr(self.message)

class ChordWeightError(Exception):
    def __init__(self, chord, message):
        self.chord = chord
        self.message = "%s: %s" % (chord, message)
    def __str__(self):
        return repr(self.message)

class ChordMapError(Exception):
    def __init__(self, chords):
        self.chords = chords
        self.message = "These chords are mapped to but not mapped from:" + str(self.chords)
    def __str__(self):
        return self.message

class ChordMap(object):
    def __init__(self):
        self.chords = {}
        random.seed()
    def isChordValid(self, chord):
        # validate input
        areAllNotesValid = all([type(n) == int and n >= 0 and n < 128 for n in chord])
        return type(chord) == tuple and areAllNotesValid
    def isWeightValid(self, weight):
        return type(weight) == int and weight > 0
    def addChord(self, chord, nextChords):
        for c in nextChords:
            if len(c) != 2:
                raise ChordWeightError(c, "Must include weight before each chord")
            if not self.isWeightValid(c[0]):
                raise ChordWeightError(c, "Weight must be int and > 0")
        if not self.isChordValid(chord) or not all([self.isChordValid(c[1]) for c in nextChords]):
            raise ChordError(chord, "Chord must be tuple and notes must be int >= 0 and < 128")
        self.chords[chord] = nextChords
    def getUnmappedChords(self):
        return list(set([
            c[1] for cs in self.chords.values() for c in cs # list of mapped-to chords
            if c[1] not in [k for k in self.chords] # keep only those not mapped-from
        ]))
    def pickRandomChord(self, currentChord):
        cumulativeWeightChords = []
        totalWeight = 0
        for c in self.chords[currentChord]:
            totalWeight += c[0]
            cumulativeWeightChords.append((totalWeight,c[1]))
        choice = random.randrange(0,totalWeight)
        for c in cumulativeWeightChords:
            if choice < c[0]:
                return c[1]

    def generateProgression(self, length, startChord):
        if self.getUnmappedChords():
            raise ChordMapError(self.getUnmappedChords())
        if type(length) != int:
            raise TypeError("'length' must be an integer")
        if length < 1:
            raise ValueError("'length' must be >= 1")
        if not self.isChordValid(startChord):
            raise ChordError(startChord, "Chord must be tuple and notes must be int >= 0 and < 128")
        random.seed()
        prog = [startChord]
        for i in range(length):
            prog.append(self.pickRandomChord(prog[-1]))
        return prog

