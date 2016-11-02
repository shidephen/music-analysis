# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 15:15:48 2016

@author: shidephen
"""

import numpy as np
import copy
from scipy import linalg
from music21 import note, stream, midi
from tone import gen_scales_seq, music21_tone_map


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
    """
    按照特定长度切割旋律音符
    :param notes: 音符序列
    :param length_in_quarter: 以4分音符标记的切割长度
    :return:
    """
    sliced = []

    ahead, remain = notes.splitAtQuarterLength(length_in_quarter)
    sliced.append(ahead)
    # ahead.plot()

    while remain.quarterLength > length_in_quarter:
        ahead, remain = remain.splitAtQuarterLength(length_in_quarter)
        # ahead.plot()
        sliced.append(ahead)

    sliced.append(remain)
    # remain.plot()
    return sliced


def score_melody_clip(melody_seq, chord_seq, bar_size=4):
    """
    为旋律与和弦匹配评分
    按照完全和弦内音时值总和除以拍数
    旋律和和弦序列的小节数必须匹配
    :param melody_seq: 旋律音符序列
    :param chord_seq: 和弦序列
    :param bar_size: 一小节长度
    :return: 匹配度
    """
    i_quarter = 0
    score = 0
    chord_len = len(chord_seq)

    for n in melody_seq:
        if not n.isClassOrSubclass((note.Note,note.Rest)):
            continue

        if n.isClassOrSubclass((note.Rest,)):
            i_quarter += n.quarterLength
            continue

        i_chord = min(int(i_quarter) / bar_size, chord_len - 1)  # assume 4 beats in a section
        i_n = music21_tone_map.tolist().index(n.name)
        root = chord_seq[i_chord]
        scales = gen_scales_seq(root, 'major')[[0, 2, 4, 6]]  # the 1st 3rd 5th 7th level is accepted
        if i_n in scales:
            score += n.quarterLength
        i_quarter += n.quarterLength

    return score / chord_len / bar_size


def match_melody_clips(clips, chords, climax_info, count):
    """
    按照评分规则选择最优的旋律片段凑成高潮部分
    :param chords: 和弦信息
    :param clips: 旋律片段
    :param climax_info: 高潮信息
    :param count: 生成的旋律排序元素个数
    :return: (总分, 生成的最优旋律)
    """
    grain = 4 # 4 bars

    chord_seq = chords[:, 1]
    chord_beats = chords[:, 0]

    climax_start = climax_info[0]
    # climax_end = climax_info[-1]
    climax_len = len(climax_info)
    chord_seq_len = len(chord_seq)
    total_score = 0

    # search for the 1st chord at the begining of climax
    i_chord = 0
    for i in range(len(chord_beats)):
        if abs(chord_beats[i] - climax_start) <= 1:
            i_chord = i

    bin_size = climax_len / grain

    C = np.zeros((len(clips), bin_size), dtype=np.int)  # clips id matrix
    S = np.zeros(C.shape)  # scores matrix corresponding to C

    clip_weights = np.zeros(len(clips))

    for i in range(0, climax_len, grain):
        # 1. find next 4 chord roots
        chords = chord_seq[i_chord : min(i_chord + grain, chord_seq_len - 1)]

        # 2. score clips for these chords

        """ !deprecated
        In order to select unused clip
        initial a clip weights with 1.0
        if a clip is chosen, weight corresponding to the clip will decrease by negtive exp
        """

        for j in range(len(clips)):
            C[j, i/grain] = clips[j].clip_id # fill in clip id
            # default: notes in the 1st part of midi file
            try:
                clip_notes = midi.translate.midiFilePathToStream(clips[j].path)[0]
                S[j, i/grain] = np.exp(-clip_weights[j]) * score_melody_clip(clip_notes, chords)
            except:
                S[j, i / grain] = 0

        i_chord += grain

    sorted_idx = np.argsort(-S, 0)
    row_size = min(count, len(clips))
    C_sorted = np.zeros((row_size, bin_size))
    S_sorted = np.zeros(C_sorted.shape)

    for i in range(bin_size):
        C_sorted[:, i] = C[:, i][sorted_idx[:row_size, i]]
        S_sorted[:, i] = S[:, i][sorted_idx[:row_size, i]]

    return C_sorted, S_sorted
