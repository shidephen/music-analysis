# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 14:28:03 2016

@author: shidephen
"""

import os, os.path
import pydub


def convert2wav(dir):
    for root, sub, files in os.walk(dir):
        for file in files:
            filepath = os.path.abspath(os.path.join(root, file))
            if filepath.endswith('mp3'):
                print('converting %s\n' % filepath)
                pos = filepath.rfind('.')
                outputfile = filepath[0: pos] + '.wav'
                clip = pydub.AudioSegment.from_file(filepath)
                clip.export(outputfile, format='wav')
                os.remove(filepath)

