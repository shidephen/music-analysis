# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 15:15:48 2016

@author: shidephen
"""
from music21 import *

from chords import extract_chord_seq
from melody import match_melody_clips
from tempo import get_climax, detect_tempo
from tone import tone_map
import numpy as np
import os


def convert2midi(notes, tempo_rate):
    m = tempo.MetronomeMark(number=tempo_rate)
    p = instrument.Piano()
    t = meter.TimeSignature('4/4')

    s = stream.Part()
    s.append(p)
    s.append(m)
    s.append(t)

    for n in s.notesAndRests:
        s.append(n)

    return s


def main():
    key = 4
    output_dir = r'music_midi\output'
    basschroma = np.loadtxt(r'Bogdan_-_01_-_Pressure_Correlation_basschroma.csv', delimiter=',', skiprows=1)
    beatline = np.loadtxt(r'Bogdan_-_01_-_Pressure_Correlation_beat.txt')
    tempo_rate = detect_tempo(beatline)
    _b, chords = extract_chord_seq(basschroma, beatline, 4)
    o = np.array([beatline[_b], tone_map[chords]])
    np.savetxt(r'Bogdan_-_01_-_Pressure_Correlation_chords.txt', o.T, fmt='%s')

    climax_info = get_climax(r'Bogdan_-_01_-_Pressure_Correlation_info.txt')

    scores = []
    file_paths = []
    clips = []
    for dirpath, dirnames, filenames in os.walk(r'music_midi\theme'):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            p = midi.translate.midiFilePathToStream(full_path)
            score, clip = match_melody_clips(p[0], chords, _b, climax_info)
            file_paths.append(full_path)
            scores.append(score)

            out_file = os.path.join(output_dir, filename.replace('.mid', '_o.mid'))
            mf = midi.translate.streamToMidiFile(clip.flat)
            mf.open(out_file, 'wb')
            mf.write()
            mf.close()

    scores = np.array(scores)
    file_paths = np.array(file_paths)
    sorted_idx = np.argsort(-scores)

    p = np.array([scores[sorted_idx], file_paths[sorted_idx]])

    np.savetxt(r'output.txt', p.T, fmt='%s', delimiter='\t\t\t\t')


if __name__ == '__main__':
    main()
