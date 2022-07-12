#! /usr/bin/env python
"""
[find the interval and duration about SWS and REM related]

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
import uOSBlib as ulib
from scipy import stats



if __name__ == '__main__':

    ulib.create_data_from_raw()
    states = {}
    for f in os.listdir(ulib.path_data['work']):
        if f.endswith(".csv"):
            
            with open(ulib.path_data['work']+f, 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
                for row in spamreader:
                    if f not in states:
                        states[f] = []
                    states[f].append(row)

    with open(ulib.path_data['processed']+'sws_before_rem_intervals.csv', mode='w', newline='') as csvfile:
        result_interval_file = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        result_interval_file.writerow(['SWS-like','REM-like'])

        for l in states:
            s_t = []
            sws_last = False
            sws_related = []
            rem_related = []
            for s in states[l]:
                if s[0] == 'SWS-like':
                    s_t = s
                    sws_last = True
                elif s[0] == 'REM-like' and sws_last :
                    sws_related.append(s_t)
                    rem_related.append(s)
                else:
                    sws_last = False
            for i in range(len(sws_related)-1):
                result_interval_file.writerow([ulib.get_interval_in_seconds(sws_related[i][2],sws_related[i+1][1]),ulib.get_interval_in_seconds(rem_related[i][2],rem_related[i+1][1])])

    with open(ulib.path_data['processed']+'sws_before_rem_duration.csv', mode='w', newline='') as csvfile:
        result_duration_file = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        s_t = []
        sws_last = False

        result_duration_file.writerow(['SWS-like','REM-like'])

        for l in states:
            for s in states[l]:

                if s[0] == 'SWS-like':
                    s_t = s
                    sws_last = True
                elif s[0] == 'REM-like' and sws_last :
                    result_duration_file.writerow([ulib.get_interval_in_seconds(s_t[1],s_t[2]),ulib.get_interval_in_seconds(s[1],s[2])])
                else:
                    sws_last = False
