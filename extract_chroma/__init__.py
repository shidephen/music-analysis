# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 17:01:37 2016

@author: shidephen
"""

import subprocess
import os

exe = os.path.join(os.path.dirname(__file__), 'extractchroma.exe')


def gen_chroma(filepath):
    command = '%s %s' % (exe, filepath)
    chroma = str(filepath).replace('.wav', '_chroma.csv')
    basschroma = str(filepath).replace('.wav', '_basschroma.csv')

    if os.path.exists(chroma) and os.path.exists(basschroma):
        return chroma, basschroma

    subprocess.call(command)
    return chroma, basschroma
