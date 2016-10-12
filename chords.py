# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 17:01:37 2016

@author: shidephen
"""

import numpy as np
from tempo import SAMPLING_RATE, BLOCK_SIZE
from tone import gen_scales_seq


def gen_bass_seq(basschroma_file):
    """
    从basschroma中生成按照最大值生成bassline
    :param basschroma_file:
    :return:
    """
    bass_chroma = np.loadtxt(basschroma_file, delimiter=',', skiprows=1)
    timestamp = bass_chroma[:, 0]
    notes = bass_chroma[:, 1:]
    bassline = notes.max(axis=1)

    return np.array([timestamp, bassline]).transpose()


def extract_chord_seq(basschroma, beatline, key, bar_size=4):
    """
    提取和弦序列
    :param basschroma: basschroma (带时间)
    :param beatline: 拍号时基
    :param bar_size: 小节大小(拍)
    :return: (拍号序列, 根音序列)
    """

    interval = BLOCK_SIZE / SAMPLING_RATE
    basschroma_length = len(basschroma)
    beats_count = len(beatline)

    scales = gen_scales_seq(key, 'major')

    timestamps = basschroma[:, 0]
    chroma = basschroma[:, 1:]

    chords_seq = []
    beats_seq = []

    i, b = 0, 0
    while b < beats_count:
        while i < basschroma_length:
            # search for a bar' start position
            if np.abs(beatline[b] - timestamps[i]) <= interval:
                break
            i += 1

        # estimate chord root in range -4 chromas to +16 chromas
        r = range(max(0, i - 3), min(i + 16, basschroma_length - 1), 1)
        det = chroma[r]
        root = np.argmax(np.sum(det, axis=0))

        if root in scales:
            chords_seq.append(root)
            beats_seq.append(b)

        b += bar_size

    return beats_seq, chords_seq
