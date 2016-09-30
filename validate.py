# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 17:01:37 2016

@author: shidephen
"""

import pydub
import os, os.path
from extract_chroma import gen_chroma
from tonality import detect_tonality
import pandas as pd
import numpy as np
import argparse


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


def test(src, key_file):
    v_keys = pd.read_csv(key_file)
    sorted_vkeys = v_keys.sort_values(by='Music')
    sorted_ckeys = src.sort_values(by='Music')
    c_key = sorted_ckeys['Key']
    t_key = sorted_vkeys['Key']
    total = t_key.count()
    compared = c_key == t_key
    accuracy = np.sum(compared)
    return float(accuracy) / total


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m',
                        '--music',
                        dest='music_path')

    return parser.parse_args()


def main(args):
    r_key = []
    r_files = []
    r_keyname = []

    convert2wav(args.music_path)
    print('Validate directory %s..\n' % args.music_path)

    for root, sub, files in os.walk(args.music_path):
        for file in files:
            filepath = os.path.abspath(os.path.join(root, file))

            if not filepath.endswith('wav'):
                continue

            print('===========================================================================================\n')
            chroma, basschroma = gen_chroma(filepath)

            key, keyname = detect_tonality(chroma)
            print('Detected file %s in key %s\n' % (filepath, keyname))

            print('===========================================================================================\n')

            pos = file.rfind('.')
            file_name = file[0:pos]
            r_files.append(file_name)
            r_key.append(int(key))
            r_keyname.append(keyname)

    result = {'Music': pd.Series(r_files), 'Key': pd.Series(r_key), 'KeyName': pd.Series(r_keyname)}
    result = pd.DataFrame(result)
    
    key_file = os.path.join(args.music_path, 'Key.txt')
    ac = test(result, key_file)
    
    print('Accuracy: %f %%' % (ac*100))
    
    result.to_csv('result.csv')


if __name__ == '__main__':
    args = parse_args()
    main(args)
