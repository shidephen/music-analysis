# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 17:01:37 2016

@author: shidephen
"""

import argparse

from config import *
import os

def parse_args():
    parser = argparse.ArgumentParser()

    # 伴奏用参数
    parser.add_argument('-m',
                        '--music',
                        dest='music_path',
                        default=None,
                        help=u'伴奏文件路径')

    parser.add_argument('-s',
                        '--style',
                        dest='style',
                        default='None',
                        help=u'伴奏风格')

    parser.add_argument('-i',
                        '--info',
                        dest='info',
                        default=None,
                        help=u'伴奏info文件')

    # 旋律MIDI用参数
    parser.add_argument('-c',
                        '--clip',
                        dest='clip_path',
                        default=None,
                        help=u'旋律文件目录')

    return parser.parse_args(), parser


def warmup_check():
    """
    检查数据库和目录情况
    :return:
    """
    if not os.path.exists(PARENT_DIR):
        print(u'需要创建存取伴奏的目录，参看config.py')
        return False

    try:
        import db
        session = db.Session()
        session.query(db.MusicInfo).all()
    except Exception as ex:
        print(u'数据库访问异常\n%s' % ex.message)
        return False

    if not os.path.exists(MUSIC_PATH):
        os.mkdir(MUSIC_PATH)
    if not os.path.exists(CLIP_PATH):
        os.mkdir(CLIP_PATH)
    if not os.path.exists(MATRIX_PATH):
        os.mkdir(MATRIX_PATH)
    if not os.path.exists(CHROMA_PATH):
        os.mkdir(CHROMA_PATH)

    return True


def main(args, parser):
    if not warmup_check():
        exit(-1)
        return False

    if args.music_path is not None:
        from processing import process_music

        print('Processing music: %s' % args.music_path)

        return process_music(args.music_path, args.info, args.style)

    if args.clip_path is not None:
        from processing import process_clip

        print('Processing clips: %s' % args.clip_path)

        for root, dirnames, filenames in os.walk(args.clip_path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                process_clip(file_path)
        return True

    parser.print_help()
    return False


if __name__ == '__main__':
    args, parser = parse_args()
    main(args, parser)
