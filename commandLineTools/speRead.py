#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Command-line tool to be called to plot a spectrum in SPE 2 or SPE 3 format (from Princeton)
# 
# Created by R. Proux, 18/01/2018

import pylab as pl
import click
import tools.instruments.princeton3.SPE2read as spe2
import tools.instruments.princeton3.SPE3read as spe3
from importlib import reload

reload(spe3)

@click.command()
@click.argument('filename', type=click.Path(exists=True))
def spe_read(filename):

    try:
        data = spe3.SPE3map(filename)
    except:
        data = spe2.SPE2map(filename)
    pl.figure()
    pl.plot(data.wavelength, data.data[0][0])
    pl.xlabel('Wavelength (nm)')
    pl.ylabel('Intensity (counts/{:.3f} s)'.format(data.exposureTime))
    pl.show()

if __name__ == '__main__':
    spe_read(r'/Users/raphaelproux/Desktop/kspace-experiment/DATA/InSe/180112-InSe-fresh-batch-S6GM1/spectra/SPOT-B/180112-S6GM1-FlakeB1-thin-INT-2s-step-glue-700-1100nm-EXC-532nm-0.20V1E3.spe')