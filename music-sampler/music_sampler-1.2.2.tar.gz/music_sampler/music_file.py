import threading
import pydub
import time
from transitions.extensions import HierarchicalMachine as Machine

import os.path

import audioop

from .lock import Lock
from .helpers import Config, gain, debug_print, error_print
from .mixer import Mixer
from .music_effect import GainEffect

file_lock = Lock("file")

class MusicFile:
    STATES = [
        'initial',
        'loading',
        'failed',
        {
            'name': 'loaded',
            'children': [
                'playing',
                'paused',
                'stopping'
            ]
        }
    ]
    TRANSITIONS = [
        {
            'trigger': 'load',
            'source': 'initial',
            'dest': 'loading',
            'after': 'poll_loaded'
        },
        {
            'trigger': 'fail',
            'source': 'loading',
            'dest': 'failed'
        },
        {
            'trigger': 'success',
            'source': 'loading',
            'dest': 'loaded'
        },
        {
            'trigger': 'start_playing',
            'source': 'loaded',
            'dest': 'loaded_playing',
            # if a child has no transitions, then it is bubbled to the parent,
            # and we don't want that. Not useful in that machine precisely.
            'conditions': ['is_loaded']
        },
        {
            'trigger': 'pause',
            'source': 'loaded_playing',
            'dest': 'loaded_paused'
        },
        {
            'trigger': 'unpause',
            'source': 'loaded_paused',
            'dest': 'loaded_playing'
        },
        {
            'trigger': 'stop_playing',
            'source': ['loaded_playing','loaded_paused'],
            'dest': 'loaded_stopping'
        },
        {
            'trigger': 'stopped',
            'source': '*',
            'dest': 'loaded',
            'before': 'trigger_stopped_events',
            'conditions': ['is_in_use']
        }
    ]

    def __init__(self, filename, mapping, name=None, gain=1):
        Machine(model=self, states=self.STATES,
                transitions=self.TRANSITIONS, initial='initial',
                ignore_invalid_triggers=True)

        self.loaded_callbacks = []
        self.mapping = mapping
        self.filename = filename
        self.name = name or filename
        self.audio_segment = None
        self.initial_volume_factor = gain
        self.music_lock = Lock("music__" + filename)

        threading.Thread(name="MSMusicLoad", target=self.load).start()

    def reload_properties(self, name=None, gain=1):
        self.name = name or self.filename
        if gain != self.initial_volume_factor:
            self.initial_volume_factor = gain
            self.reload_music_file()

    def reload_music_file(self):
        with file_lock:
            try:
                if self.filename.startswith("/"):
                    filename = self.filename
                else:
                    filename = Config.music_path + self.filename

                debug_print("Reloading « {} »".format(self.name))
                initial_db_gain = gain(self.initial_volume_factor * 100)
                self.audio_segment = pydub.AudioSegment \
                        .from_file(filename) \
                        .set_frame_rate(Config.frame_rate) \
                        .set_channels(Config.channels) \
                        .set_sample_width(Config.sample_width) \
                        .apply_gain(initial_db_gain)
            except Exception as e:
                error_print("failed to reload « {} »: {}"\
                        .format(self.name, e))
                self.loading_error = e
                self.to_failed()
            else:
                debug_print("Reloaded « {} »".format(self.name))

    # Machine related events
    def on_enter_loading(self):
        with file_lock:
            try:
                if self.filename.startswith("/"):
                    filename = self.filename
                else:
                    filename = Config.music_path + self.filename

                debug_print("Loading « {} »".format(self.name))
                self.mixer = self.mapping.mixer or Mixer()
                initial_db_gain = gain(self.initial_volume_factor * 100)
                self.audio_segment = pydub.AudioSegment \
                        .from_file(filename) \
                        .set_frame_rate(Config.frame_rate) \
                        .set_channels(Config.channels) \
                        .set_sample_width(Config.sample_width) \
                        .apply_gain(initial_db_gain)
                self.sound_duration = self.audio_segment.duration_seconds
            except Exception as e:
                error_print("failed to load « {} »: {}".format(self.name, e))
                self.loading_error = e
                self.fail()
            else:
                self.success()
                debug_print("Loaded « {} »".format(self.name))

    def on_enter_loaded(self):
        self.cleanup()

    def cleanup(self):
        self.gain_effects = []
        self.set_gain(0, absolute=True)
        self.current_audio_segment = None
        self.volume = 100
        self.wait_event = threading.Event()
        self.current_loop = 0

    def on_enter_loaded_playing(self):
        self.mixer.add_file(self)

    # Machine related states
    def is_in_use(self):
        return self.is_loaded(allow_substates=True) and not self.is_loaded()

    def is_in_use_not_stopping(self):
        return self.is_loaded_playing() or self.is_loaded_paused()

    # Machine related triggers
    def trigger_stopped_events(self):
        self.mixer.remove_file(self)
        self.wait_event.set()
        self.cleanup()

    # Actions and properties called externally
    @property
    def sound_position(self):
        if self.is_in_use():
            return self.current_frame / self.current_audio_segment.frame_rate
        else:
            return 0

    def play(self, fade_in=0, volume=100, loop=0, start_at=0):
        self.set_gain(gain(volume) + self.mapping.master_gain, absolute=True)
        self.volume = volume
        if loop < 0:
            self.last_loop = float('inf')
        else:
            self.last_loop = loop

        with self.music_lock:
            self.current_audio_segment = self.audio_segment
            self.current_frame = int(start_at * self.audio_segment.frame_rate)

        self.start_playing()

        if fade_in > 0:
            db_gain = gain(self.volume, 0)[0]
            self.set_gain(-db_gain)
            self.add_fade_effect(db_gain, fade_in)

    def seek(self, value=0, delta=False):
        if not self.is_in_use_not_stopping():
            return

        with self.music_lock:
            self.abandon_all_effects()
            if delta:
                frame_count = int(self.audio_segment.frame_count())
                frame_diff = int(value * self.audio_segment.frame_rate)
                self.current_frame += frame_diff
                while self.current_frame < 0:
                    self.current_loop -= 1
                    self.current_frame += frame_count
                while self.current_frame > frame_count:
                    self.current_loop += 1
                    self.current_frame -= frame_count
                if self.current_loop < 0:
                    self.current_loop = 0
                    self.current_frame = 0
                if self.current_loop > self.last_loop:
                    self.current_loop = self.last_loop
                    self.current_frame = frame_count
            else:
                self.current_frame = max(
                        0,
                        int(value * self.audio_segment.frame_rate))

    def stop(self, fade_out=0, wait=False, set_wait_id=None):
        if self.is_loaded_playing():
            ms = int(self.sound_position * 1000)
            ms_fo = max(1, int(fade_out * 1000))

            new_audio_segment = self.current_audio_segment[: ms+ms_fo] \
                .fade_out(ms_fo)
            with self.music_lock:
                self.current_audio_segment = new_audio_segment
            self.stop_playing()
            if wait:
                if set_wait_id is not None:
                    self.mapping.add_wait_id(set_wait_id, self.wait_event)
                self.wait_end()
        else:
            self.stopped()

    def abandon_all_effects(self):
        db_gain = 0
        for gain_effect in self.gain_effects:
            db_gain += gain_effect.get_last_gain()

        self.gain_effects = []
        self.set_gain(db_gain)

    def set_volume(self, value, delta=False, fade=0):
        [db_gain, self.volume] = gain(
                value + int(delta) * self.volume,
                self.volume)

        self.set_gain_with_effect(db_gain, fade=fade)

    def set_gain_with_effect(self, db_gain, fade=0):
        if not self.is_in_use():
            return

        if fade > 0:
            self.add_fade_effect(db_gain, fade)
        else:
            self.set_gain(db_gain)

    def wait_end(self):
        self.wait_event.clear()
        self.wait_event.wait()

    # Let other subscribe for an event when they are ready
    def subscribe_loaded(self, callback):
        # FIXME: should lock to be sure we have no race, but it makes the
        # initialization screen not showing until everything is loaded
        if self.is_loaded(allow_substates=True):
            callback(True)
        elif self.is_failed():
            callback(False)
        else:
            self.loaded_callbacks.append(callback)

    def poll_loaded(self):
        for callback in self.loaded_callbacks:
            callback(self.is_loaded())
        self.loaded_callbacks = []

    # Callbacks
    def finished_callback(self):
        self.stopped()

    def play_callback(self, out_data_length, frame_count):
        if self.is_loaded_paused():
            return b'\0' * out_data_length

        with self.music_lock:
            [data, nb_frames] = self.get_next_sample(frame_count)
            if nb_frames < frame_count:
                if self.is_loaded_playing() and\
                        self.current_loop < self.last_loop:
                    self.current_loop += 1
                    self.current_frame = 0
                    [new_data, new_nb_frames] = self.get_next_sample(
                            frame_count - nb_frames)
                    data += new_data
                    nb_frames += new_nb_frames
                elif nb_frames == 0:
                    # FIXME: too slow when mixing multiple streams
                    threading.Thread(
                            name="MSFinishedCallback",
                            target=self.finished_callback).start()

            return data.ljust(out_data_length, b'\0')

    # Helpers
    def set_gain(self, db_gain, absolute=False):
        if absolute:
            self.db_gain = db_gain
        else:
            self.db_gain += db_gain

    def get_next_sample(self, frame_count):
        fw = self.audio_segment.frame_width

        data = b""
        nb_frames = 0

        segment = self.current_audio_segment
        max_val = int(segment.frame_count())

        start_i = max(self.current_frame, 0)
        end_i   = min(self.current_frame + frame_count, max_val)
        data += segment._data[start_i*fw : end_i*fw]
        nb_frames += end_i - start_i
        self.current_frame += end_i - start_i

        volume_factor = self.volume_factor(self.effects_next_gain(nb_frames))

        data = audioop.mul(data, Config.sample_width, volume_factor)

        return [data, nb_frames]

    def add_fade_effect(self, db_gain, fade_duration):
        if not self.is_in_use():
            return

        self.gain_effects.append(GainEffect(
            "fade",
            self.current_audio_segment,
            self.current_loop,
            self.sound_position,
            self.sound_position + fade_duration,
            gain=db_gain))

    def effects_next_gain(self, frame_count):
        db_gain = 0
        for gain_effect in self.gain_effects:
            [new_gain, last_gain] = gain_effect.get_next_gain(
                    self.current_frame,
                    self.current_loop,
                    frame_count)
            if last_gain:
                self.set_gain(new_gain)
                self.gain_effects.remove(gain_effect)
            else:
                db_gain += new_gain
        return db_gain


    def volume_factor(self, additional_gain=0):
        return 10 ** ( (self.db_gain + additional_gain) / 20)

