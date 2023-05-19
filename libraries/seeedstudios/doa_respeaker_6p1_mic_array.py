# -*- coding: utf-8 -*-

"""
Time Difference of Arrival for ReSpeaker USB Mic Array (6 plus 1)
@author: xiongyihui for Seeed Studio: https://raw.githubusercontent.com/voice-engine/voice-engine/master/voice_engine/doa_respeaker_6p1_mic_array.py
"""

import collections
import numpy as np

from .element import Element
from .gcc_phat import gcc_phat


SOUND_SPEED = 340.0

MIC_DISTANCE_6P1 = 0.064
MAX_TDOA_6P1 = MIC_DISTANCE_6P1 / float(SOUND_SPEED)


class DOA(Element):
    def __init__(self, rate=16000, chunks=50):
        super(DOA, self).__init__()

        self.queue = collections.deque(maxlen=chunks)
        self.sample_rate = rate

        self.pair = [[1, 4], [2, 5], [3, 6]]

    def put(self, data):
        self.queue.append(data)

        super(DOA, self).put(data)

    def get_direction(self):
        tau = [0, 0, 0]
        theta = [0, 0, 0]

        buf = b''.join(self.queue)
        buf = np.fromstring(buf, dtype='int16')
        for i, v in enumerate(self.pair):
            tau[i], _ = gcc_phat(buf[v[0]::8], buf[v[1]::8], fs=self.sample_rate, max_tau=MAX_TDOA_6P1,
                                 interp=1)
            theta[i] = np.arcsin(tau[i] / MAX_TDOA_6P1) * 180 / np.pi

        min_index = np.argmin(np.abs(tau))
        if (min_index != 0 and theta[min_index - 1] >= 0) or (min_index == 0 and theta[len(self.pair) - 1] < 0):
            best_guess = (theta[min_index] + 360) % 360
        else:
            best_guess = (180 - theta[min_index])

        best_guess = (best_guess + 120 + min_index * 60) % 360

        return best_guess
