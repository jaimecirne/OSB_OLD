#! /usr/bin/env python
"""
states Count


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


def get_first_mode(a):
    c = Counter(a)  
    mode_count = max(c.values())
    mode = {key for key, count in c.items() if count == mode_count}
    first_mode = next(x for x in a if x in mode)
    return first_mode

if __name__ == '__main__':

    for f in os.listdir("./data"):
        if f.endswith(".csv"):
            print("Data from "+f)
            with open("./data/"+f, 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
                for row in spamreader:
                    states.append(row)
                states_len = len(states)

            for s in states:

                if s[0] not in state_intervals:
                    classStates.append(s[0])
                    state_counter[s[0]] = 1
                    hour = int(s[2].split(':')[0])
                    minutes = int(s[2].split(':')[1])
                    seconds = int(s[2].split(':')[2])
                    state_intervals[s[0]] = {0 : hour*3600  + minutes*60 + seconds}

                    # print (str(hour)+" "+str(minutes)+" "+str(seconds))

                    # print("Estado "+str(s[0])+" intervalo "+str(state_intervals[s[0]])+" aberto ou fechado"+str(interval_opened[s[0]]))

                else:
                    i = len(state_intervals[s[0]])-1

                    if state_counter[s[0]] % 2 != 0:
                        hour = int(s[1].split(':')[0])
                        minutes = int(s[1].split(':')[1])
                        seconds = int(s[1].split(':')[2])
                
                
                        # print("Estado "+str(s[0])+" intervalo "+str(state_intervals[s[0]][i])+" aberto ou fechado"+str(interval_opened[s[0]]))

                        # print(str(hour*3600  + minutes*60 + seconds) +" - "+str(state_intervals[s[0]][i]))

                        # print (hour*3600  + minutes*60 + seconds - state_intervals[s[0]][i])

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


            # print(classStates)

            # print(state_intervals)

            # remove elements that presented just one time  
            [state_intervals.pop(c) for c in classStates if state_counter[c] == 1]

            [classStates.remove(c) for c in classStates if state_counter[c] == 1]


            # print(state_intervals)

            file_result = open(f+".txt", "w")
            

            for c in classStates:

                state_interval = state_intervals[c]

                state_interval_list = [s for s in state_interval.values()]

                interval = 1
                # media = statistics.median(rmL1)

                mode = get_first_mode(state_interval_list)
                tekilaList = []

                for i in state_interval:
                    aux = int(i % mode)	
                    # print(abs(mode + interval))
                    if int(state_interval[i]) <= (abs(mode + interval)) and int(state_interval[i]) >= (abs(mode - interval)):
                        tekilaList.extend(state_interval_list)

                print("Total "+str(c)+" intervals = ", len(state_interval))
                print("Mode = ", mode)
                print("Total intervals above or below {} minutes = {}".format(interval, len(tekilaList)))
                print("Percent {}/{} = {}%".format(len(tekilaList), len(state_interval), round((len(tekilaList)/len(state_interval)*100),2)))
                print(tekilaList)

                file_result.write("Total "+str(c)+" intervals = "+str(len(state_interval)))
                file_result.write("\n")
                file_result.write("Mode = "+str(mode))
                file_result.write("\n")
                file_result.write("Total intervals above or below "+str(interval)+" minutes = "+ str(len(tekilaList)))
                file_result.write("\n")
                file_result.write("Percent "+str(len(tekilaList))+" /"+str(len(state_interval))+" = "+str(round((len(tekilaList)/len(state_interval)*100),2))+"%")
                file_result.write("\n")
                file_result.write(str(tekilaList))
                file_result.write("\n")
                file_result.write("\n")

            file_result.close()
