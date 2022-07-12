#! /usr/bin/env python
"""
[find the interval and duration about SWS and REM related and create a img]

"""
# Authors: Jaime Bruno Cirne de Oliveira (jaime@neuro.ufrn.br)

from __future__ import division

from collections import Counter
import sys
import csv
import statistics
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import uOSBlib as ulib
from scipy import stats



if __name__ == '__main__':

    sizefone = 18

    ulib.create_data_from_raw()
    
    sws_durations = []
    rem_durations = []
    with open(ulib.path_data['processed']+'sws_before_rem_duration.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            if row[0] != 'SWS-like':
                sws_durations.append(int(row[0]))
                rem_durations.append(int(row[1]))

    linregress = stats.linregress(sws_durations,rem_durations)

    coef = np.polyfit(sws_durations,rem_durations,1)
    poly1d_fn = np.poly1d(coef) 

    plt.suptitle("Line Regress SWS-like and REM-like related",fontname='Arial', size=sizefone+2, weight="bold")
    plt.plot(sws_durations,rem_durations, 'ko', sws_durations, poly1d_fn(sws_durations), '--b',alpha=0.8)
    plt.ylabel("Duration of REM-like (seconds)", fontname='Arial',size=sizefone, weight="bold")    
    plt.xlabel("Duration of SWS-like (seconds)", fontname='Arial',size=sizefone, weight="bold")
    plt.xticks( fontname='Arial', size=sizefone-2, weight="bold")
    plt.yticks( fontname='Arial', size=sizefone-2, weight="bold")

    #plt.annotate(linregress[], (0,0), (0, -20), xycoords='axes fraction', textcoords='offset points', va='top')
    plt.show()

    print(linregress)

