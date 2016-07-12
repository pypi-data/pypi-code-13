import os
import io
import wave
from os import path

import speech_recognition as sr


def _patch_get_wave(number_channels):
    def inner(self, convert_rate=None, convert_width=None):
        raw_data = self.get_raw_data(convert_rate, convert_width)
        sample_rate = self.sample_rate if convert_rate is None else convert_rate
        sample_width = self.sample_width if convert_width is None else convert_width

        with io.BytesIO() as wav_file:
            with wave.open(wav_file, 'wb') as f:
                f.setframerate(sample_rate)
                f.setsampwidth(sample_width)
                f.setnchannels(number_channels)
                f.writeframes(raw_data)
                wav_data = wav_file.getvalue()

        return wav_data
    return inner


class SpeechText:
    def __init__(self, google_api_key):
        self.recognizer = sr.Recognizer()
        self._api_key = google_api_key
        self._number_channels = None

    def get_msg(self, data, rate, sample_width, number_channels):
        sr.AudioData.get_wav_data = _patch_get_wave(number_channels)
        audio_data = sr.AudioData(data, rate, sample_width)

        msg = self.recognizer.recognize_google(audio_data,
                                               key=self._api_key,
                                               show_all=True)

        return msg
