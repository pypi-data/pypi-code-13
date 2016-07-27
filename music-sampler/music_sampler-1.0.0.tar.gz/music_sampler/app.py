from .helpers import parse_args, register_fonts, duration_to_min_sec, path

parse_args()

import kivy
kivy.require("1.9.1")
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ListProperty, StringProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from .key import Key
from .mapping import Mapping

register_fonts()

class KeyList(RelativeLayout):
    keylist = ListProperty([])
    first_key = StringProperty("")
    second_key = StringProperty("")
    third_key = StringProperty("")

    def append(self, value):
        self.keylist.insert(0, value)

    def on_keylist(self, instance, new_key_list):
        if len(self.keylist) > 0:
            self.first_key  = self.keylist[0]
        if len(self.keylist) > 1:
            self.second_key = self.keylist[1]
        if len(self.keylist) > 2:
            self.third_key  = self.keylist[2]

class PlayList(RelativeLayout):
    playlist = ListProperty([])

    def __init__(self, **kwargs):
        super(PlayList, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_playlist, 0.5)

    def update_playlist(self, dt):
        if self.parent is None or 'Mapping' not in self.parent.ids:
            return True

        open_files = self.parent.ids['Mapping'].open_files
        self.playlist = []
        for music_file in open_files.values():
            if not music_file.is_in_use():
                continue

            text = "{}/{}".format(
                    duration_to_min_sec(music_file.sound_position),
                    duration_to_min_sec(music_file.sound_duration))

            if music_file.is_loaded_paused():
                self.playlist.append(["⏸", music_file.name, text, False])
            else:
                self.playlist.append(["⏵", music_file.name, text, True])


class ActionList(RelativeLayout):
    action_title = StringProperty("")
    action_list = ListProperty([])

    def update_list(self, key, action_descriptions):
        self.action_title = "actions linked to key {}:".format(key.key_sym)
        self.action_list = []

        for [action, status] in action_descriptions:
            if status == "done":
                icon = "✓"
            elif status == "current":
                icon = "✅"
            else:
                icon = " "
            self.action_list.append([icon, action])

class Screen(FloatLayout):
    pass

class MusicSamplerApp(App):
    def build(self):
        Window.size = (913, 563)

        return Screen()

def main():
    Builder.load_file(path() + "/music_sampler.kv")
    MusicSamplerApp().run()
