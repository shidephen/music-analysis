# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 17:01:37 2016

@author: shidephen
"""
import numpy as np

tone_map = np.array(
    ['A', 'Bb', 'B', 'C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab'])

music21_tone_map = np.array([
    'A', 'B-', 'B', 'C', 'C#', 'D', 'E-', 'E', 'F', 'F#', 'G', 'G#'
])

music21_tone_dict = {
    'A':0, 'B-':1, 'B':2, 'C':3,
    'C#':4, 'D':5, 'E-':6, 'E':7,
    'F':8, 'F#':9, 'G':10, 'G#':11,
    'A-':11
}

major_scale = [2, 2, 1, 2, 2, 2]
minor_scale = [2, 1, 2, 2, 1, 2]


def gen_scales_seq(root, key):
    """
    生成以root为主音的7级
    :param root: 主音
    :param key: 调性('major', 'minor')
    :return: 以A开始的数字序列
    """
    seq = list()
    seq.append(root)

    if key == 'major':
        scales = major_scale
    else:
        scales = minor_scale

    for tone in scales:
        root = (root + tone) % 12
        seq.append(root)

    return np.array(seq)


def shift_root_seq(root):
    """
    生成以root为根音的12个音阶
    :param root: 根音
    :return: 以A开始的数字序列
    """
    pass

