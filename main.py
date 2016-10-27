# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 17:01:37 2016

@author: shidephen
"""

import argparse
from processing import process_clip, process_music
from config import *


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m',
                        '--music',
                        dest='music_path',
                        default=None)

    parser.add_argument('-c',
                        '--clip',
                        dest='clip_path',
                        default=None)

    return parser.parse_args()


def warmup_check():
    pass


def main(args):
    if args.music_path is not None:
        print('Processing music: %s' % args.music_path)
        process_music(args.music_path)

    if args.clip_path is not None:
        print('Processing clips: %s' % args.clip_path)
        process_clip(args.clip_path)

if __name__ == '__main__':
    args = parse_args()
    main(args)
