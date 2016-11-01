# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 14:28:03 2016

@author: shidephen
"""

import os, os.path
from pydub import AudioSegment
from music21 import *


def convert2wav(filepath):
    """
    将音频文件转换成wav
    :param filepath: 文件路径
    :return: 输出文件路径， 文件时长
    """
    if not os.path.exists(filepath):
        return None, 0

    if filepath.endswith('.wav'):
        clip = AudioSegment.from_file(filepath)
        return filepath, clip.duration_seconds

    pos = filepath.rfind('.')
    outputfile = filepath[0: pos] + '.wav'
    clip = AudioSegment.from_file(filepath)
    clip.export(outputfile, format='wav')
    # os.remove(filepath)
    return outputfile, clip.duration_seconds


def construct_midi(notes, tempo_rate):
    """
    将音符流转化成MIDI文件
    :param notes: 音符
    :param tempo_rate: BPM
    :return:
    """
    m = tempo.MetronomeMark(number=tempo_rate)
    p = instrument.Piano()
    t = meter.TimeSignature('4/4')

    s = stream.Part()
    s.append(p)
    s.append(t)
    s.append(m)

    for n in s.notesAndRests:
        s.append(n)

    return s

