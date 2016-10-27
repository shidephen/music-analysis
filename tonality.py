# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 17:01:37 2016

@author: shidephen
"""

import numpy as np
from scipy import linalg
from tone import tone_map, gen_scales_seq


def _move_major_key(root, chroma_sum, tone_idx):
    semi4 = (root + 3) % 12  # 小3度
    semi5 = (root + 4) % 12  # 3度
    i_semi4 = 0; i_semi5 = 0; i = 0

    for tone in tone_idx:
        if tone == semi4:
            i_semi4 = i
        elif tone == semi5:
            i_semi5 = i
        i += 1

    # chroma_static = {'Chroma': pd.Series(chroma_sum[np.argsort(-chroma_sum)])}
    chroma_static = pd.DataFrame(chroma_sum[np.argsort(-chroma_sum)],
                                 index=tone_map[np.argsort(-chroma_sum)],
                                 columns=['Chroma'])

    print(chroma_static)
    print('\n')

    # 3度强于小3度为大调
    if i_semi5 < i_semi4:
        root = (root + 3) % 12

    M7 = (root + 11) % 12  # 大7度
    m7 = (root + 10) % 12  # 小7度
    t4 = (root + 5) % 12  # 4度
    f6 = (root + 6) % 12  # 增4度
    i_M7 = 0; i_m7 = 0; i_M4 = 0; i_a4 = 0; i = 0

    for tone in tone_idx:
        if tone == M7:
            i_M7 = i
        elif tone == m7:
            i_m7 = i
        elif tone == t4:
            i_M4 = i
        elif tone == f6:
            i_a4 = i

        i += 1

    """
    大调前提下：
    1. 大七度大于小七度 并且 四度大于增四度时换调
    2. 大七度大于小七度 并且 四度小于增四度时变为5度音
    3. 大七度小于小七度 并且 四度大于增四度时变为4度音
    4. 其他情况不能判断， 保持不变
    """
    scales = gen_scales_seq(root, 'major')

    shifted_root = [(x + root) % 12 for x in range(12)]
    print('Major levels: %s \nMajor scales: %s\n' % (tone_map[scales], tone_map[shifted_root]))
    print(chroma_static.loc[tone_map[shifted_root]])
    print('\n')

    if i_M7 > i_m7 and i_M4 > i_a4:
        return root
    if i_M7 > i_m7 and i_M4 < i_a4:
            return scales[4]
    if i_M7 < i_m7 and i_M4 > i_a4:
        return scales[3]
    return root


def detect_tonality(chroma, norm_ord=None):
    """
    根据chroma信息检测歌曲调性
    :param chroma: chroma 数组
    :param norm_ord: 标准化选项，同norm函数
    :return: (调性， 调字符表示)
    """
    chroma = chroma[:, 1:]
    if norm_ord is None:        
        chroma_sum = np.mean(chroma)
        chroma_sum = chroma_sum[1:]
        chroma_sum = np.array(chroma_sum)
    else:
        chroma_sum = np.empty([12])
        for c in chroma:
            semi = c[1:]
            n = linalg.norm(semi, ord=norm_ord)
            if n == 0:
                continue
            
            chroma_sum = chroma_sum + (semi / n)

    scores = []
    for t in range(12):
        levels = gen_scales_seq(t, 'major')
        score = np.sum(chroma_sum[levels])
        scores.append(score)
        
    scores = np.array(scores)
    
    print('Scores: \n%s\n%s\n' % (tone_map, scores))
    
    sorted_idx = np.argsort(-scores)
    
    print('Sorted:\n %s\n%s\n' % (tone_map[sorted_idx], scores[sorted_idx]))
    
    # sorted_idx = np.argsort(chroma_sum)
    root = np.argmax(scores)

    # root = _move_major_key(root, chroma_sum, sorted_idx)

    return root, tone_map[root]
    
    
def move_key_to(notes, src_key, dest_key):
    pass
