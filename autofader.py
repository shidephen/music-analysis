# -*- coding: utf-8 -*-
"""
自动响度框架
Author: shidephen
"""
import numpy as np
from scipy.io import wavfile
import os
from scipy.signal import lfilter
import sys
from matplotlib import pyplot as plt

eps = np.finfo(np.float32).eps
USE_FILTER = False


def weight_filter(x):
    # Filter 1
    B = [1.176506, -2.353012, 1.176506]
    A = [1, -1.960601, 0.961086]
    x_filtered = lfilter(B, A, x)
    # Filter 2
    B = [0.951539, -1.746297, 0.845694]
    A = [1, -1.746297, 0.797233]
    x_filtered = lfilter(B, A, x_filtered)
    # Filter 3
    B = [1.032534, -1.42493, 0.601922]
    A = [1, -1.42493, 0.634455]
    x_filtered = lfilter(B, A, x_filtered)
    # Filter 4
    B = [0.546949, -0.189981, 0.349394]
    A = [1, -0.189981, -0.103657]
    x_filtered = lfilter(B, A, x_filtered)

    return x_filtered


def measure_loudness(x, fs, tao=0.035, k=0.85, use_filter=False):
    """
    计算响度特征
    :param x:
    :param fs:
    :param tao:
    :param k:
    :return:
    """

    # N = fs / 4
    N = 4096
    c = np.exp(-1.0 / tao / fs)

    if use_filter:
        x_filtered = weight_filter(x) # weighted loudness
    else:
        x_filtered = x # Flat unit

    Vms = np.zeros(len(x_filtered))
    Vms[0] = (1 - c) * (x_filtered[0]**2)

    for i in range(1, len(Vms)):
        Vms[i] = c * Vms[i-1] + (1 - c) * (x_filtered[i]**2)

    Vrms = np.sqrt(Vms[np.arange(N-1, len(Vms), N)]) + eps
    VdB = 20.0 * np.log10(Vrms)
    ui = np.exp2(-VdB * np.log2(k))
    ui_sum = np.sum(ui)
    wi = ui / ui_sum

    L = np.sum(wi*VdB)
    return L, 20 * np.log10(np.max(x)), VdB


def readwav2mono(filename):
    fs, x = wavfile.read(filename)
    if len(x.shape) > 1:
        x = (x[:, 0] + x[:, 1]) / 2

    x = x / 32768.0
    return fs, x

def calc_fader(loudness, peaks, gains):
    assert(len(loudness) == len(peaks))
    # max_loudness = np.max(loudness)
    # normalized_loudness = loudness / max_loudness
    gained_loudness = loudness + gains
    mediam_L = np.median(gained_loudness)
    # avg_L = np.mean(loudness)
    Lva = mediam_L - gained_loudness

    for i in range(len(gained_loudness)):
        abs_peak = np.abs(peaks[i])
        Lva[i] = Lva[i] if Lva[i] < abs_peak else abs_peak

    # fv_dB = 20 * np.log10(cv)
    # maximaus_fv = fv_dB - np.max(fv_dB)
    return np.round(Lva, 2)


def abs_mean(x):
    x_mean = np.mean(x)
    x_len = len(x)
    return np.sum(np.abs(x-x_mean)) / x_len


def ideal_compressor(signal, threshold, ratio, gain):
    m = len(signal)
    out_signal = np.zeros(m)
    for i in range(m):
        if signal[i] > threshold:
            if ratio==np.inf:
                out_signal[i] = threshold
            else:
                out_signal[i] = signal[i] * (2 - 1.0/ratio)
        else:
            out_signal[i] = signal[i]

    out_signal += gain
    return out_signal


def calc_compressor(peak, VdB, varian=8):
    profile_threshold = 0.99
    #ratio_threshold = 0.5
    hist, bins = np.histogram(VdB, 100)

    hist = hist / float(sum(hist))
    hist_cum = np.cumsum(hist)
    threshold = np.min(bins[hist_cum>=profile_threshold]) + 3

    # var_origin = np.std(VdB)
    ratio = np.std(VdB) / varian
    if ratio < 1:
        ratio = 1

    gain = (peak - threshold) * (1 - 1.0/ratio)

    return np.round(threshold, 2), np.round(ratio, 2), np.round(gain, 2)


def automixing(project):
    filepaths = []
    for root, dirs, files in os.walk(project):
        for file in files:
            if file.endswith('.wav'):
                filepaths.append(os.path.join(root, file))

    m = len(filepaths)
    loudness = np.zeros(m)
    peaks = np.zeros(m)
    filenames = []
    compressor_values = np.zeros((m, 3))

    # find music
    bk_music = None
    for i in range(m):
        if filepaths[i].endswith('_cut.wav'):
            bk_music = filepaths[i]
            break

    if bk_music is not None:
        filepaths.remove(bk_music)
        filepaths.insert(0, bk_music)

    # calculate loudness and compressor params
    ref_DR = 8
    for i in range(m):
        filename = os.path.split(filepaths[i])[-1]
        fs, x = readwav2mono(filepaths[i])
        if i==0 :
            loudness[i], peaks[i], VdB = measure_loudness(x, fs, use_filter=False)
            ref_DR = np.std(VdB)
            plt.figure()
            plt.hist(VdB, 100)
            plt.show()
        else:
            loudness[i], peaks[i], VdB = measure_loudness(x, fs, use_filter=USE_FILTER)

        threshold, ratio, gain = calc_compressor(peaks[i], VdB, ref_DR)
        compressor_values[i, 0] = threshold
        compressor_values[i, 1] = ratio
        compressor_values[i, 2] = gain

        print('%s @ Loudness: %f dB; peak: %f' % (filename, loudness[i], peaks[i]))
        print('%s @ Threshold: %.2f dB; Ratio: %.2f; Gain: %.2f' % (filename, threshold, ratio, gain))

        filenames.append(filename)

    faders = calc_fader(loudness, peaks, compressor_values[:, 2])
    max_fades = np.max(faders)

    # make clip
    if max_fades > 0:
        faders = faders - max_fades

    print('Faders: %s' % str(faders))

    return faders, filenames


def save2file(fv, target, filenames):
    m = len(fv)
    with open(target, 'w') as f:
        for i in range(m):
            f.writelines('%s @ %.2f\n' % (filenames[i], fv[i]))
        f.flush()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(-1)

    root = sys.argv[1]
    # root = 'project'
    faders, files = automixing(root)

    save2file(faders, root+'.txt', files)
