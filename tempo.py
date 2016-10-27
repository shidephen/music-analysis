# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 09:17:40 2016

@author: shidephen
"""

import numpy as np
from music21 import note
from tone import music21_tone_map

BLOCK_SIZE = 2048
SAMPLING_RATE = 44100.0
QUARTER_SIZE = 0.25


def detect_tempo(beatline):
    """
    计算歌曲的bpm数
    :param beatline: 包含beat信息的numpy array
    :return: bpm
    """
    p1_beats = beatline[1:]
    n1_beats = beatline[0: -1]
    offset = p1_beats - n1_beats

    return np.round(1 / np.mean(offset) * 60)


def pad_beats(notes, bpm, beat_size=QUARTER_SIZE, fs=SAMPLING_RATE, block_size=BLOCK_SIZE):
    """
    按照chroma间距填充音符中间的chroma
    :param notes: 音符
    :param bpm: 拍速
    :param beat_size: 小节数
    :param fs: 采样率
    :param block_size: 缓冲区大小
    :return:
    """

    interval = float(block_size) / fs # sampling intervals
    notes_chroma = []
    notes_count = len(notes)
    chroma_sum = 0

    for n in range(notes_count):
        """
        From statistics, the max chroma intensity for a note is about 3, the min intensity is 0.
        For a  note from midi, all chroma in a duration is 3 and for a rest is 0.
        """
        if notes[n].isClassOrSubclass((note.Note,)):
            chroma = np.zeros(12)
            chroma[np.where(music21_tone_map == notes[n].name)[0][0]] = 3
        elif notes[n].isClassOrSubclass((note.Rest,)):
            chroma = np.zeros(12)
        else:
            continue

        b = notes[n].duration.quarterLength * QUARTER_SIZE / beat_size # beat
        s = b * 60.0 / bpm # note length in second
        l = int(np.round(s / interval)) # fill length

        # print('Insert %d chromas for %s @ %.2f' % (l, notes[n].name, notes[n].offset))

        for i in range(l):
            notes_chroma.append(chroma)

        chroma_sum += l

    # print('Total insert %d chromas' % chroma_sum)
    return np.array(notes_chroma)


def get_climax(music_info):
    """
    获取高潮部分的拍号
    :param music_info: music_info文件路径
    :return:
    """
    s_climax = None
    with open(music_info) as f:
        lines = f.readlines()
        for l in lines:
            if 'Climax:' in l:
                s_climax = l

    if s_climax is None:
        return None

    s_climax = s_climax.strip()
    s_climax = s_climax[s_climax.find(':') + 1:]

    return map(lambda x: int(x), s_climax.split(','))
