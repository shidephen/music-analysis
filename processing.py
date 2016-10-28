# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 10:58:10 2016

@author: shidephen
"""
from pydub import AudioSegment
import os
import shutil
import numpy as np

from config import *
from extract_chroma import gen_chroma
from tonality import detect_tonality
from chords import extract_chord_seq
from tempo import get_climax, detect_tempo
from beat import gen_beat_file
from melody import match_melody_clips
import db

def convert2wav(filepath):
    if not os.path.exists(filepath):
        return None, 0

    if filepath.endswith('.wav'):
        clip = AudioSegment.from_file(filepath)
        return filepath, clip.duration_seconds

    pos = filepath.rfind('.')
    outputfile = filepath[0: pos] + '.wav'
    clip = AudioSegment.from_file(filepath)
    clip.export(outputfile, format='wav')
    os.remove(filepath)
    return outputfile, clip.duration_seconds

def process_music(music_path, info_path, style):
    music_name = os.path.split(music_path)[-1]
    music_name = music_name[: music_name.rfind('.')]

    music_wav, duration = convert2wav(music_path)

    # compute chroma and basschroma information
    chroma_file, basschroma_file = gen_chroma(music_wav)
    if chroma_file is None or basschroma_file is None:
        print('\nFailed to compute chroma for %s\n' % music_wav)
        return False

    chroma_out = os.path.join(CHROMA_PATH, music_name+CHROMA_SUFFIX)
    basschroma_out = os.path.join(CHROMA_PATH, music_name+BASSCHROMA_SUFFIX)

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
    # till now only use climax infomation
    info_path_new = os.path.join(MUSIC_INFO_PATH, music_name+INFO_SUFFIX)
    shutil.move(info_path, info_path_new)
    climax = get_climax(info_path_new)

    assert(len(chroma) > 0)
    assert(len(basschroma) > 0)
    assert(len(beatline) > 0)
    assert(climax is not None and len(climax) > 0)

    print('\nComputed chroma and beats.\n')

    # Compute Beats per minute
    bpm = detect_tempo(beatline)

    # Compute tonality
    key, keyname = detect_tonality(chroma)

    # Estimate chords
    chords = extract_chord_seq(basschroma, beatline, key)

    # connect to database
    session = None
    try:
        session = db.Session()
    except Exception as ex:
        print('\nError connecting to database %s, %s\n'
              % (CONNECTION_STRING, ex.message))

    assert(session is not None)
    # fetch all clips in the same key
    clips = session.query(db.ClipInfo).filter(db.ClipInfo.key == key).all()

    # compute clip scores
    C, S = match_melody_clips(clips, chords, climax, 10)

    print('\nClip IDs matrix:\n%s' % C)
    print('\nClip scores matrix:%s\n' % S)

    Cmatrix_path = os.path.join(MATRIX_PATH, music_name+ID_MATRIX_SUFFIX)
    Smatrix_path = os.path.join(MATRIX_PATH, music_name+SCORES_MATRIX_SUFFIX)

    np.savetxt(Cmatrix_path, C)
    np.savetxt(Smatrix_path, S)

    info = db.MusicInfo()
    info.name = music_name
    info.time = duration
    info.style = style
    info.bpm = bpm
    info.key = key
    info.music_path = music_path

    # delete temp chroma files
    if os.path.exists(chroma_file):
        os.remove(chroma_file)
    if os.path.exists(basschroma_file):
        os.remove(basschroma_file)
    if os.path.exists(chroma_out):
        os.remove(chroma_out)
    if os.path.exists(basschroma_out):
        os.remove(basschroma_out)
    if not music_path.endswith('.wav'):
        os.remove(music_wav)

    return True


def process_clip(clip_path):
    pass
