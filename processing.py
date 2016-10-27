# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 10:58:10 2016

@author: shidephen
"""
from extract_chroma import gen_chroma
from pydub import AudioSegment
import os
import shutil
from config import *

from tonality import detect_tonality
from chords import extract_chord_seq
from tempo import get_climax, detect_tempo
from beat import gen_beat_file
import numpy as np
import db

def convert2wav(filepath):
    pos = filepath.rfind('.')
    outputfile = filepath[0: pos] + '.wav'
    clip = AudioSegment.from_file(filepath)
    clip.export(outputfile, format='wav')
    os.remove(filepath)
    return outputfile

def process_music(music_path):
    music_wav = music_path
    if not music_path.endswith('.wav'):
        music_wav = convert2wav(music_path)

    # compute chroma and basschroma information
    chroma_file, basschroma_file = gen_chroma(music_wav)
    if chroma_file is None or basschroma_file is None:
        print('\nFailed to compute chroma for %s\n' % music_wav)
        return False

    chroma_out = os.path.join(CHROMA_PATH, os.path.split(chroma_file)[-1])
    basschroma_out = os.path.join(CHORD_PATH, os.path.split(basschroma_file)[-1])

    shutil.move(chroma_file, chroma_out)
    shutil.move(basschroma_file, basschroma_out)

    # Compute tempo infomation
    beat_file = gen_beat_file(music_wav, BEAT_PATH)
    if beat_file is None:
        print('\nFailed to compute beat info for %s\n' % music_wav)
        return False

    # Load computed information
    chroma = np.loadtxt(chroma_out, delimiter=',', skiprows=1)
    basschroma = np.loadtxt(basschroma_out, delimiter=',', skiprows=1)
    beatline = np.loadtxt(beat_file)

    assert(len(chroma) > 0)
    assert(len(basschroma) > 0)
    assert(len(beatline) > 0)

    print('\nComputed chroma and beats.\n')

    # Compute Beats per minute
    bpm = detect_tempo(beatline)

    # Compute tonality
    key, keyname = detect_tonality(chroma)

    # Estimate chords
    chord_beats, chords_seq = extract_chord_seq(basschroma, beatline, key)

    # connect to database
    session = None
    try:
        session = db.Session()
    except Exception as ex:
        print('\nError connecting to database %s, %s\n'
              % (CONNECTION_STRING, ex.message))

    # fetch all clips in the same key
    assert(session is not None)
    session.query(db.ClipInfo).filter(db.ClipInfo.key == key).all()

    # delete temp chroma files
    if os.path.exists(chroma_file):
        os.remove(chroma_file)
    if os.path.exists(basschroma_file):
        os.remove(basschroma_file)
    if os.path.exists(chroma_out):
        os.remove(chroma_out)
    if os.path.exists(basschroma_out):
        os.remove(basschroma_out)



def process_clip(clip_path):
    pass
