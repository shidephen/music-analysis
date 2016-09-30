# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 09:48:31 2016

@author: shidephen
"""

import os
import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn import linear_model as lm
import argparse


def load_chroma(chroma_path):
    chroma_info = np.loadtxt(chroma_path, delimiter=',', skiprows=1)
    chroma_sum = np.sum(chroma_info, axis=0)
    chroma_sum = chroma_sum[1:]
    return chroma_sum


def load_chroma_dir(chroma_dir):
    chroma = []
    audio_files = []
    for root, sub, files in os.walk(chroma_dir):
        for filename in files:
            if not filename.endswith('csv'):
                continue
            
            file_path = os.path.join(root, filename)            
            chroma_info = np.loadtxt(file_path, delimiter=',', skiprows=1)
            chroma_sum = np.sum(chroma_info, axis=0)
            chroma_sum = chroma_sum[1:]
            chroma.append(chroma_sum)
            
            pos = filename.rfind('_')
            audio_files.append(filename[0: pos])
            
    audio_files = np.array(audio_files)
    chroma = np.array(chroma)    
    sorted_idx = np.argsort(audio_files)
    
    return chroma[sorted_idx], audio_files[sorted_idx] 
    

def load_key(key_path):
    keys_df = pd.read_csv(key_path)
    keys = np.array(keys_df['Key'])
    files = np.array(keys_df['Music'])
    
    sorted_idx = np.argsort(files)
    
    return keys[sorted_idx]
    
    
def train_svm(key_file, chroma_dir):
    cf = SVC(kernel='linear')
    y = load_key(key_file)
    X, f = load_chroma_dir(chroma_dir)
    
    cf.fit(X, y)
    
    return cf


def train_logistic(key_file, chroma_dir):
    y = load_key(key_file)
    X, f = load_chroma_dir(chroma_dir)
    
    lr = lm.LogisticRegression()
    lr.fit(X, y)
    
    return lr
    
    
def test(model, key_file, chroma_dir):
    t_y = load_key(key_file)
    t_X, f = load_chroma_dir(chroma_dir)
    
    return model.score(t_X, t_y)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-t',
                        '--train',
                        dest='train')
                        
    parser.add_argument('-v',
                        '--validate',
                        dest='validate')

    return parser.parse_args()


def main(args):
    print('Training in %s\n' % args.train)
    
    key_file = os.path.join(args.train, 'Key.txt')
    model = train_logistic(key_file, args.train)
    
    print('Coefficients:\n')
    print(model.coef_)
    print('\n')
    
    key_file = os.path.join(args.validate, 'Key.txt') 
    accuracy = test(model, key_file, args.validate)
    print('Accurarcy: %f' % (float(accuracy) * 100))


if __name__ == '__main__':
    args = parse_args()
    main(args)

