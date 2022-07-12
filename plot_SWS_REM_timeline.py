#! /usr/bin/env python
"""
time line histogram SWS


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
import itertools
from scipy import stats
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d
# micro OSB lib verify if there is a uOSBfile in the same path
import uOSBlib as ulib


def plot_sws_rem_timeline(files_list, animal):
    
    sws_duration = {}
    rem_duration = {}

    sws_start = {}
    rem_start = {}

    for f in files_list:

            states = []

            with open(ulib.path_data['work']+f, 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
                for row in spamreader:
                    states.append(row)

            s_t = []
            sws_last = False

            A = f.split('.')[0]
            D = f.split('.')[1]
            M = f.split('.')[2]
            Y = '20'+((f.split('.')[3]).split('-')[0])

            P = A+Y+M+D

            for s in states:
                
                if s[0] == 'SWS-like':
                    s_t = s
                    sws_last = True
                elif s[0] == 'REM-like' and sws_last:
                    if P not in sws_duration:
                        sws_duration[P] = [ulib.get_duration_in_seconds(s_t[1], s_t[2])]
                        rem_duration[P] = [ulib.get_duration_in_seconds(s[1], s[2])]
                        sws_start[P] = [s_t[1]]
                        rem_start[P] = [s[1]]
                    else:
                        sws_duration[P].append(ulib.get_duration_in_seconds(s_t[1], s_t[2]))
                        rem_duration[P].append(ulib.get_duration_in_seconds(s[1], s[2]))
                        sws_start[P].append(s_t[1])
                        rem_start[P].append(s[1])
                else:
                    sws_last = False

    n_bins = 100
    intervals =  [len(sws_duration[x]) for x in sws_duration]
    intervals.insert(0,0)

    rmL = []
    rmL2 = []

    labels_sws = []
    labels_rem = []

    labels_sws.insert(0,0)
    labels_rem.insert(0,0)

    for s in sws_duration:
        rmL.extend(sws_duration[s])

    for s in rem_duration:
        rmL2.extend(rem_duration[s])

    for s in sws_start:
        labels_sws.extend(sws_start[s])

    for s in rem_start:
        labels_rem.extend(rem_start[s])

    box = [sws_duration[x] for x in sws_duration]

    histo, bin_edges = np.histogram(rmL, bins=n_bins)
    aux = gaussian_filter1d(histo, sigma=0.5)
    histrmL = bin_edges, aux

    print('histo')
    print(histo)
    print('aux')
    print(aux)
    print('histrml')
    print(histrmL)
    print('bin_edges')
    print(bin_edges)


    # # ==========================================================================================
    # #                   	Graph
    yMin = min(rmL)
    yMax = max(rmL)
    histoyMin = min(histrmL[0])
    histoyMax = max(histrmL[0])
    histoxMin = min(histrmL[1])
    histoxMax = max(histrmL[1])
    ylim = [yMin -5, yMax+5]
    xticks = np.arange(0,len(rmL)+1,1)
    yticks = np.arange(1,len(rmL)+1)
    yticks1 = np.arange(0,3300,120)

    yticksHisto = np.arange(0,100,10)
    sizefone = 18
    dt = 0.5
    tam = 0.3
    color = ['#4169E1','#1E90FF','#00BFFF','#87CEFA']
    labelsBox = ['Paçoca', 'Pipa','Marshmallow', 'Ary']

    plt.subplots_adjust(top=0.88, bottom=0.11, 
        left=0.12, right=0.90, hspace=0.20, wspace=0.20)

 
    plt.suptitle("Duration of SWS-like before a REM-like of "+animal,fontname='Arial', size=sizefone+2, weight="bold")
    
#   plt.subplot(2,4,(1,3))
    plt.xlim([0,len(rmL)+1])
    plt.ylim(ylim)
    plt.axvspan(intervals[0], intervals[1], facecolor=color[0], alpha=0.5)
    plt.axvspan(intervals[1], intervals[1] + intervals[2], facecolor=color[1], alpha=0.5)
    plt.axvspan(intervals[1] + intervals[2], intervals[1] + intervals[2] + intervals[3], facecolor=color[2], alpha=0.5)
    plt.axvspan(intervals[1] + intervals[2] + intervals[3], len(rmL)+1, facecolor=color[3], alpha=0.5)
    plt.scatter(yticks, rmL,  color='black')
    plt.scatter(yticks, rmL2,  color='red')
    plt.xticks(xticks, labels_rem, fontname='Arial', size=sizefone-2, weight="bold")
    plt.yticks(yticks1, fontname='Arial', size=sizefone-2, weight="bold")
    plt.ylabel("Duration of SWS-like (seconds)", fontname='Arial',size=sizefone, weight="bold")

    # plt.savefig("test_rasterization.png", dpi=300)
    plt.show()

if __name__ == '__main__':
    
    ulib.create_data_from_raw()

    files_p2 = [ f for f in os.listdir(ulib.path_data['work']) if f.endswith(".csv") and f.startswith('p2')]
    files_p3 = [ f for f in os.listdir(ulib.path_data['work']) if f.endswith(".csv") and f.startswith('p3')]
    files_p4 = [ f for f in os.listdir(ulib.path_data['work']) if f.endswith(".csv") and f.startswith('p4')]
    files_p5 = [ f for f in os.listdir(ulib.path_data['work']) if f.endswith(".csv") and f.startswith('p5')]

    plot_sws_rem_timeline(files_p2,'Paçoca')
    plot_sws_rem_timeline(files_p3,'Pipa') 
    plot_sws_rem_timeline(files_p4,'Marshmallow')
    plot_sws_rem_timeline(files_p5,'Ary')