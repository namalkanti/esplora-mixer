import sys
import time
import wave

import numpy as np
import scipy as sp

from pyaudio import PyAudio, paContinue

DEFAULT_SAVE1 = 0
DEFAULT_SAVE2 = -1

class OutputAudioStream():
    """
    Class to handle real time audio stream for mixer.
    """

    def __init__(self, file_name, esplora):
        """
        Constructor takes in file name and loads into array for playback.
        Also takes in esplora state generator.
        """
        self._pyaudio = PyAudio()
        self._esplora = esplora
        self._save_one = DEFAULT_SAVE1
        self._save_two = DEFAULT_SAVE2
        self._audio = wave.open(file_name, "rb")


    def playback(self):
        """
        Plays back audio stream while taking input from explora.
        """
        esplora = self._esplora

        def callback(in_data, frame_count, time_info, flag):
            if flag:
                print("Playback Error: {0}".format(flag))
                sys.exit(1)
            data = next(esplora)
            print(data)
            data = self._audio.readframes(frame_count)
            return (data, paContinue)


        stream = self._pyaudio.open(format = self._pyaudio.get_format_from_width(self._audio.getsampwidth()),
                channels = self._audio.getnchannels(),
                rate = self._audio.getframerate(),
                output = True,
                frames_per_buffer = 1024,
                stream_callback = callback)

        while stream.is_active():
            time.sleep(0.1)

        stream.close()

    def close(self):
        """
        Closes pyaudio object.
        """
        self._audio.close()
        self._pyaudio.terminate()
