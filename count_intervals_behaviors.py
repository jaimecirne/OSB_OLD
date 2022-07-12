#! /usr/bin/env python
"""
Count Intervals Behaviors


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
from scipy import stats
# micro OSB lib verify if there is a uOSBfile in the same path
import uOSBlib as ulib

if __name__ == '__main__':

    ulib.create_data_from_raw()

    ulib.print_error_time()

    for f in os.listdir(ulib.path_data['work']):
        if f.endswith(".csv"):

            states = []
            classStates = []
            state_intervals = {}
            counter = {}
            open_intervals = {}
            
            with open(ulib.path_data['work']+f, 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
                for row in spamreader:
                    if any(row):
                        states.append(row)

            for s in states:
                if s[0] not in open_intervals:
                    counter[s[0]] = 1
                    state_intervals[s[0]] = {}

                if s[0] in open_intervals :
                    hour = int(s[1].split(':')[0])
                    minutes = int(s[1].split(':')[1])
                    seconds = int(s[1].split(':')[2])
                    i = len(state_intervals[s[0]])
                    state_intervals[s[0]][i] = ulib.str_time_to_int_seconds(s[1]) - open_intervals[s[0]]
                    classStates.append(s[0])

                open_intervals[s[0]] = ulib.str_time_to_int_seconds(s[2])

                counter[s[0]] = counter[s[0]]+1

            for c in classStates:
                with open(ulib.path_data['splited']+c+'_'+f, mode='w', newline='') as csvfile:
                    result_file = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    state_interval = state_intervals[c]
                    state_interval_list = [s for s in state_interval.values()]
                    for sil in state_interval_list:
                        result_file.writerow([sil])

    state_intervals = {}
    classStates = []

    for f in os.listdir(ulib.path_data['splited']):
        if f.endswith(".csv"):
            classe = str(f.split('_')[0])

            if classe not in classStates:
                    classStates.append(classe)

            with open(ulib.path_data['splited']+f, 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
                for row in spamreader:
                    if classe in state_intervals:
                        state_intervals[classe].extend(row)
                    else:
                        state_intervals[classe] = row

    for c in classStates:
        state_interval_list = state_intervals[c]
        with open(ulib.path_data['byclass']+c+'_intervals.csv', mode='w', newline='') as csvfile:
            result_file = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            state_interval_list = state_intervals[c]
            for s in state_interval_list:
                result_file.writerow([s])

    for c in classStates:
        state_interval = state_intervals[c]
        with open(ulib.path_data['processed']+c+'_.csv', mode='w', newline='') as csvfile:
            result_file = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            state_interval_list = state_intervals[c]
            sl = len(state_interval_list)
        
            #data = Counter(state_interval_list)  
            #dic_data = dict(data)
            #mode = [k for k, v in dic_data.items() if v == max(list(data.values()))]
            
            result_file.writerow(['Intervals of '+str(c)])
            result_file.writerow(state_interval_list)
            result_file.writerow(['Intervals mode of '+str(c)])
            
            mode_interval = stats.mode(state_interval_list)

            range_1m = 60
            range_5m = 300
            range_10m = 600
            mode_around_1m = []
            mode_around_5m = []
            mode_around_10m = []
            
            mode_i = int(mode_interval[0][0])
            
            result_file.writerow(stats.mode(state_interval_list))

            for sl in state_interval_list:
                i = int(sl)
                if i <= mode_i + range_1m and i >= mode_i - range_1m:
                    mode_around_1m.append(sl)
                elif  i <= mode_i + range_5m and i >= mode_i - range_5m:
                    mode_around_5m.append(sl)
                elif  i <= mode_i + range_10m and i >= mode_i - range_10m:
                    mode_around_10m.append(sl)
            
            result_file.writerow(['Intervals mode around 1m'])
            result_file.writerow(mode_around_1m)

            result_file.writerow(['Intervals mode around 5m'])
            result_file.writerow(mode_around_5m)

            result_file.writerow(['Intervals mode around 10m'])
            result_file.writerow(mode_around_5m)

            #result_file.writerow(['Standard Deviation of '+str(c)])
            #result_file.writerow(statistics.stdev(state_interval_list))
            #result_file.writerow([statistics.stdev(state_interval_list)])
            #print("Meam of  is % s "% (statistics.mean(state_interval_list)))
            #print("Standard Deviation of  is % s "% (statistics.stdev(state_interval_list)))

print("Done")