# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 17:01:37 2016

@author: shidephen
"""

# Output directories
PARENT_DIR = r'D:\Last'
MUSIC_PATH = PARENT_DIR + r'\Songs'
CLIP_PATH = PARENT_DIR + r'\Clips'
CHORD_PATH = PARENT_DIR + r'\Songs'
BEAT_PATH = PARENT_DIR + r'\Songs'
MATRIX_PATH = PARENT_DIR + r'\Data'
MUSIC_INFO_PATH = PARENT_DIR + r'\Songs'

# Naming suffices
CHROMA_SUFFIX = '_chroma.csv'
BASSCHROMA_SUFFIX = '_basschroma.csv'
BEAT_SUFFIX = '_beat.txt'
INFO_SUFFIX = '_info.txt'
CHORD_SUFFIX = '_chord.txt'
# clip id and its score matrix
ID_MATRIX_SUFFIX = '_clips.txt'
SCORES_MATRIX_SUFFIX = '_scores.txt'

# Temparay data directories
CHROMA_PATH = PARENT_DIR + r'\Temp'

# database connection
CONNECTION_STRING = 'mysql://root:tuya2016@localhost/music_db'
