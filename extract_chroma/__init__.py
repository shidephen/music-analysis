# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 17:01:37 2016

@author: shidephen
"""

import subprocess
import os

exe = os.path.join(os.path.dirname(__file__), 'extractchroma.exe')


def gen_chroma(filepath):
    """
    生成音频chroma信息
    :param filepath: 音频文件路径(必须是wav)
    :return: chroma文件路径(chroma, basschroma)
    """
    assert(filepath.endswith('.wav'))
    command = '%s %s' % (exe, filepath)
    chroma = str(filepath).replace('.wav', '_chroma.csv')
    basschroma = str(filepath).replace('.wav', '_basschroma.csv')

    if os.path.exists(chroma) and os.path.exists(basschroma):
        return chroma, basschroma

    ret = subprocess.call(command)
    if ret != 0:
        return None, None

    return chroma, basschroma
