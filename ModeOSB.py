#! /usr/bin/env python
"""
StatisticsOSB


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

states = []
classStates = []
state_intervals = {}
state_counter = {}
states_len = 0


if __name__ == '__main__':

    for f in os.listdir("./dataraw"):
        if f.endswith(".csv"):
            print("Data from "+f)
            with open("./dataraw/"+f, 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
                for row in spamreader:
                    states.append(row)
                states_len = len(states)

            print(states)

            for s in states:

                if s[0] not in state_intervals:
                    classStates.append(s[0])
                    state_counter[s[0]] = 1
                    hour = int(s[2].split(':')[0])
                    minutes = int(s[2].split(':')[1])
                    seconds = int(s[2].split(':')[2])
                    state_intervals[s[0]] = {0 : hour*3600  + minutes*60 + seconds}

                else:
                    i = len(state_intervals[s[0]])-1

                    if state_counter[s[0]] % 2 != 0:
                        hour = int(s[1].split(':')[0])
                        minutes = int(s[1].split(':')[1])
                        seconds = int(s[1].split(':')[2])

                        interval = hour*3600  + minutes*60 + seconds - state_intervals[s[0]][i]

                        if interval > 0:
                            state_counter[s[0]] = state_counter[s[0]]+1
                            state_intervals[s[0]][i] = interval

                    else:
                        hour = int(s[2].split(':')[0])
                        minutes = int(s[2].split(':')[1])
                        seconds = int(s[2].split(':')[2])
                        state_counter[s[0]] = state_counter[s[0]]+1
                        state_intervals[s[0]][i+1] = hour*3600  + minutes*60 + seconds

            # print(state_intervals)

            # remove elements that presented just one time  
            [state_intervals.pop(c) for c in classStates if state_counter[c] == 1]

            [classStates.remove(c) for c in classStates if state_counter[c] == 1]

            for c in classStates:

                state_interval = state_intervals[c]

                state_interval_list = [s for s in state_interval.values()]

                sl = len(state_interval_list)
                
                data = Counter(state_interval_list)  
                dic_data = dict(data)
                mode = [k for k, v in dic_data.items() if v == max(list(data.values()))]


                if len(mode) == sl: 
                    print(str(c))
                    print("No mode found in ")
                else: 
                    print(str(c))
                    print("Mode is / are: " + ', '.join(map(str, mode))) 

