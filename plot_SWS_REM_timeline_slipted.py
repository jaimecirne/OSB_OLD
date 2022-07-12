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


def plot_sws_rem_timeline(files_list):
    
    all = True

    sws_duration = {}
    rem_duration = {}

    sws_start = {}
    rem_start = {}
    animal = ''
    D = ''
    M = ''
    Y = ''
    color = {'p2':'#4169E1','p3':'#1E90FF','p4':'#00BFFF','p5':'#87CEFA'}
    labelsBox = {'p2':'Paçoca', 'p3':'Pipa','p4':'Marshmallow', 'p5':'Ary'}

    for f in files_list:

            states = []

            with open(ulib.path_data['work']+f, 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
                for row in spamreader:
                    states.append(row)

            s_t = []
            sws_last = False

            animal = f.split('.')[0]
            D = f.split('.')[1]
            M = f.split('.')[2]
            Y = '20'+((f.split('.')[3]).split('-')[0])

            P = animal+Y+M+D

            for s in states:
                
                if all:
                    
                    if s[0] == 'SWS-like':
                        if P not in sws_duration:
                            sws_duration[P] = [ulib.get_duration_in_seconds(s[1], s[2])]
                            sws_start[P] = [s[1]]
                        else:
                            sws_duration[P].append(ulib.get_duration_in_seconds(s[1], s[2]))
                            sws_start[P].append(s[1])
                    if s[0] == 'REM-like':
                        if P not in sws_duration:
                            rem_duration[P] = [ulib.get_duration_in_seconds(s[1], s[2])]
                            rem_start[P] = [s[1]]
                        else:
                            rem_duration[P].append(ulib.get_duration_in_seconds(s[1], s[2]))
                            rem_start[P].append(s[1])

                else:
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

    if len(sws_duration) > 0 and len(rem_duration) > 0:

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

        intervals = [len(rmL)+1]
        intervals.insert(0,0)

        box = [sws_duration[x] for x in sws_duration]


        # # ==========================================================================================
        # #                   	Graph
        yMin = min(rmL)
        yMax = max(rmL)

        ylim = [yMin -5, yMax+5]
        xticks = np.arange(0,len(rmL)+1,1)
        yticks = np.arange(1,len(rmL)+1)
        yticks1 = np.arange(0,3300,120)

        yticksHisto = np.arange(0,100,10)
        sizefone = 18
        dt = 0.5
        tam = 0.3
        
        

        plt.subplots_adjust(top=0.88, bottom=0.11, 
            left=0.12, right=0.90, hspace=0.20, wspace=0.20)

    
        plt.suptitle("Duration of SWS-like before a REM-like of "+labelsBox[animal]+' on '+M+'/'+D+'/'+Y,fontname='Arial', size=sizefone+2, weight="bold")
        
        plt.xlim([0,len(rmL)+1])
        plt.ylim(ylim)

        plt.axvspan(0, len(rmL)+1,facecolor=color[animal], alpha=0.5)

        plt.scatter(yticks, rmL,  color='black')
        plt.scatter(yticks, rmL2,  color='red')
        plt.xticks(xticks, labels_rem, fontname='Arial', size=sizefone-2, weight="bold")
        plt.yticks(yticks1, fontname='Arial', size=sizefone-2, weight="bold")
        plt.ylabel("Duration of SWS-like (seconds)", fontname='Arial',size=sizefone, weight="bold")
        plt.subplots_adjust(left=0.12, bottom=0.11, right=0.90, top=0.88, wspace=0.20, hspace=0.20)

        
        #plt.savefig(ulib.path_data['img']+labelsBox[animal]+''+M+'_'+D+'_'+Y+'.png', dpi=300, orientation='landscape', figsize=(25.600, 12.790))
        plt.show()

if __name__ == '__main__':

    ulib.init_data()

    files_p2_11 = ['p2.11.04.18-1.csv']
    files_p2_12 = ['p2.12.04.18-1.csv', 'p2.12.04.18-2.csv']
    files_p2_13 = ['p2.13.04.18-1.csv', 'p2.13.04.18-2.csv']
    files_p2_14 = ['p2.14.04.18-1.csv']
    
    files_p3_26 = ['p3.26.07.18-1.csv', 'p3.26.07.18-2.csv', 'p3.26.07.18-3.csv']
    files_p3_27 = ['p3.27.07.18-1.csv', 'p3.27.07.18-2.csv']
    files_p3_28 = ['p3.28.07.18-1.csv', 'p3.28.07.18-2.csv', 'p3.28.07.18-3.csv']
    files_p3_29 = ['p3.29.07.18-1.csv', 'p3.29.07.18-2.csv']
    
    files_p4_20 = ['p4.20.10.18-1.csv']
    files_p4_21 = ['p4.21.10.18-1.csv']
    files_p4_22 = ['p4.22.10.18-1.csv', 'p4.22.10.18-2.csv']
    files_p4_23 = ['p4.23.10.18-1.csv', 'p4.23.10.18-2.csv']
    
    files_p5_16 = ['p5.16.03.18-1.csv', 'p5.16.03.18-2.csv']
    files_p5_18 = ['p5.18.03.18-1.csv']
    files_p5_19 = ['p5.19.03.18-1.csv', 'p5.19.03.18-2.csv']
    files_p5_20 = ['p5.20.03.18-1.csv', 'p5.20.03.18-2.csv']

    plot_sws_rem_timeline(files_p2_11)
    plot_sws_rem_timeline(files_p2_12)
    plot_sws_rem_timeline(files_p2_13)
    plot_sws_rem_timeline(files_p2_14)

    plot_sws_rem_timeline(files_p3_26)
    plot_sws_rem_timeline(files_p3_27)
    plot_sws_rem_timeline(files_p3_28)
    plot_sws_rem_timeline(files_p3_29)

    plot_sws_rem_timeline(files_p4_20)
    plot_sws_rem_timeline(files_p4_21)
    plot_sws_rem_timeline(files_p4_22)
    plot_sws_rem_timeline(files_p4_23)

    plot_sws_rem_timeline(files_p5_16)
    plot_sws_rem_timeline(files_p5_18)
    plot_sws_rem_timeline(files_p5_19)
    plot_sws_rem_timeline(files_p5_20)