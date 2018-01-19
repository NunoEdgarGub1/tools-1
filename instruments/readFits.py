# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Wed Jan 18 18:50:59 2017

@author: raphaelproux

Library to read and write simple fits files with one frame to and from numpy arrays. 
If the input file is not in FITS format, the imread() function from scipy.ndimage is used (reads a lot of formats)
"""


from astropy.io import fits
import pylab as pl
from scipy.ndimage import imread
import os

def readFits(filename):
    dataToRet = None
    try:
        fitsFile = fits.open(filename)
        try:
            dataToRet = fitsFile[0].data
        finally:
            fitsFile.close()
    except:
        dataToRet = imread(filename)
    return dataToRet
    
def saveFits(filepath, data, overwrite=False):
    # strip extension from filepath
    filepath, extension = os.path.splitext(filepath)
    if extension == '':
        extension = '.fits'
    path, filename = os.path.split(filepath)
    hdu = fits.PrimaryHDU(data.astype(pl.uint16))
    
    if not overwrite:
        if os.path.exists(filepath + extension):
            i = 0
            while os.path.exists(filepath + '-{}'.format(i) + extension):
                i += 1
            filepath = filepath + '-{}'.format(i)
    
    hdu.writeto(filepath + extension, clobber=overwrite)

if __name__ == "__main__":
    measurement = readFits(r'/Users/raphaelproux/Desktop/kspace-experiment/DATA/InSe/180111-InSe-gm1/polarA2/0.tif')

    pl.figure()
    pl.imshow(measurement, vmax=500)
    pl.show()
    
    # saveFits(r'/Users/raphaelproux/Desktop/InSe-Mauro/MoSe2/170117-mose2-on-gold-no-glass-plate/real-space-doudou', measurement)
    
    