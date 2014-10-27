import sys
import time
import wave

import numpy as np
import scipy as sp

from pyaudio import PyAudio, paContinue, paInt32
from scipy.io.wavfile import read

DEFAULT_SAVE1 = 0
DEFAULT_SAVE2 = 0

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
        self._rate, self._audio = read(file_name)


    def playback(self):
        """
        Plays back audio stream while taking input from explora.
        """
        esplora = self._esplora
        counter = 0

        def callback(in_data, frame_count, time_info, flag):
            nonlocal counter, esplora
            if flag:
                print("Playback Error: {0}".format(flag))
                sys.exit(1)

            esplora_data = next(esplora)

            if esplora_data and 6 == len(esplora_data):
                if 0 == int(esplora_data[1]):
                    self._save_one = counter
                elif 0 == int(esplora_data[2]):
                    self._save_two = counter

                gain = esplora_data[0]
                
                if 0 == int(esplora_data[3]):
                    counter = self._save_one
                elif 0 == int(esplora_data[4]):
                    counter = self._save_two

                if 1 == int(esplora_data[5]):
                    counter += frame_count
                elif -1 == int(esplora_data[5]):
                    counter -= frame_count

            start = counter
            counter += frame_count
            data = self._audio[start:counter] 
            return (data, paContinue)


        stream = self._pyaudio.open(format = paInt32,
                channels = 1,
                rate = self._rate,
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
        self._pyaudio.terminate()
