#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This file contains several toolbox functions to process 1D numpy arrays - basic signal treatment, filters, etc.
# 
# Created by R. Proux, 16/10/2017

import pylab as pl
import scipy.signal

def smooth(x,window_len=11,window='hanning'):
    """smooth the data using a window with requested size.
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.

    Copied and modified from http://scipy-cookbook.readthedocs.io/items/SignalSmooth.html  (16/10/2017 - RProux)
    
    input:
        x: the input signal 
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal
        
    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)
    
    see also: 
    
    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter
 
    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: the window_len parameter should always be odd for reliable output (will shift slightly the data if even)
    """

    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")

    if window_len < 3:
        return x

    if window not in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is one of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")


    s = pl.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    print(s)
    print(len(s))
    if window == 'flat': #moving average
        w = pl.ones(window_len, 'd')
    else:
        w = eval('pl.{}(window_len)'.format(window))

    y = pl.convolve(w / w.sum(), s, mode='valid')

    return y[int(pl.floor(window_len/2)) : -int(pl.ceil(window_len/2) - 1)]


def filter_cosmic_rays(spectrum, error_thr=10., filter_size=5):
    """
    Filters out cosmic rays from a 1D spectrum (simple spike detection algorithm).
    
    Args:
        spectrum (numpy array): a 1D numpy array with spectrum data
        error_thr (float, optional): spike detection threshold. If the distance from smoothened spectrum to real 
        spectrum is greater than error_thr, data will be replaced by smoothened spectrum.
        filter_size (int, optional): number of pixels of the smoothening window.
    
    Returns:
        numpy array: the spectrum corrected (spikes removed).
    """

    spectrum_smooth = scipy.signal.medfilt(spectrum, filter_size)
    bad_pixels = pl.absolute(spectrum - spectrum_smooth) > float(error_thr)
    spectrum_corr = spectrum.copy()
    spectrum_corr[bad_pixels] = spectrum_smooth[bad_pixels]
    
    return spectrum_corr


if __name__ == '__main__':
    x = pl.linspace(0, 10, 100)
    data = pl.sin(x)

    data_smooth = smooth(data, 13)
    
    pl.figure()
    pl.plot(x, data)
    pl.plot(x, data_smooth)
    pl.plot(x, scipy.signal.medfilt(data, 5))
    pl.show()
