# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 17:01:37 2016

@author: shidephen
"""

import argparse
import tonality
import pandas as pd
from extract_chroma import gen_chroma
from tonality import detect_tonality


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-b',
                        '--basschroma',
                        dest='basschroma_path')

    parser.add_argument('-c',
                        '--chroma',
                        dest='chroma_path')

    parser.add_argument('-o',
                        '--output',
                        dest='output_path')

    return parser.parse_args()


def main(args):
    chroma = pd.read_csv(args.chroma_path)
    t, tn = tonality.detect_tonality(chroma)
    print(tn)

if __name__ == '__main__':
    args = parse_args()
    main(args)
