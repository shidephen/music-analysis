# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 15:15:48 2016

@author: shidephen
"""

import numpy as np
from scipy import linalg
from music21 import stream
from music21 import note


def cos_distance(v1, v2):
    """
    两个array的cos距离
    :param v1:
    :param v2:
    :return:
    """
    return np.sum(v1 * v2) / linalg.norm(v1, ord=2) / linalg.norm(v2, ord=2)


def scan_pos_similarity(melody_chroma, music_chroma):
    """
    扫描歌曲生成相似度序列
    :param melody_chroma: 旋律chroma序列
    :param music_chroma: 音乐chroma序列
    :return: (位置, 相似度)
    """
    music_len = len(music_chroma)
    melody_len = len(melody_chroma)

    positions = range(music_len - melody_len)
    similarity = []

    for i in positions:
        clip_chroma = music_chroma[i:i + melody_len]

        offset = cos_distance(melody_chroma, clip_chroma)

        similarity.append(offset)

    return  np.array(positions), np.array(similarity)


def split_melody(notes, length_in_quarter):
    sliced = []

    ahead, remain = notes.splitAtQuarterLength(length_in_quarter)
    sliced.append(ahead)
    ahead.plot()

    while remain.quarterLength > length_in_quarter:
        ahead, remain = remain.splitAtQuarterLength(length_in_quarter)
        ahead.plot()
        sliced.append(ahead)

    sliced.append(remain)
    remain.plot()
    return sliced