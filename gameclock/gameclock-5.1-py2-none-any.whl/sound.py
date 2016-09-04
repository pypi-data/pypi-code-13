# -*- coding: utf-8 -*-

import os


class AudioDriverException(Exception):
    pass


# basic sound support, depends on python-pygame and sound-theme-freedesktop
class Player:
    def __init__(self, sounds, callback=None):
        """initializes the audio engine with a list of sounds. the
        callback is called to see if we can play sounds, allows for
        disabling the engine live."""
        self.sounds = {}
        self.callback = callback
        import pygame
        from pygame import mixer
        try:
            mixer.init()
        except pygame.error as e:
            raise AudioDriverException("%s" % e)
        else:
            for sound, filename in sounds.iteritems():
                if os.path.exists(filename):
                    self.sounds[sound] = mixer.Sound(filename)
                else:
                    raise IOError('sound file "%s" not found: %s'
                                  % (sound, filename))

    def play(self, sound):
        if self.callback():
            self.sounds[sound].play()


class DumbPlayer:
    def play(self, sound):
        pass
