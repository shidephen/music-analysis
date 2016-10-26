# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 11:10:19 2016

@author: shidephen
"""
import subprocess
import os.path

# beatroot jar
beat_root = os.path.join(os.path.dirname(__file__), 'beatroot.jar')


def gen_beat_file(music_path, output_dir):
    """
    生成歌曲的beat信息
    :param music_path: 歌曲路径(必须是wav)
    :param output_dir: beat文件输出目录
    :return: beat文件路径
    """
    assert (music_path.endswith('.wav'))

    if not os.path.exists(music_path):
        return None

    filename = os.path.split(music_path)[-1]
    filename = filename.replace('.wav', '_beat.txt')
    filepath = os.path.join(output_dir, filename)

    ret = subprocess.call(['java', '-jar', beat_root,
                           '-o', filepath,
                           music_path])

    if int(ret) != 0:
        return None

    return filepath
