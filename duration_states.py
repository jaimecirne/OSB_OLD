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

    for f in os.listdir(ulib.path_data['work']):
        if f.endswith(".csv"):
            states = []
            with open(ulib.path_data['work']+f, 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
                for row in spamreader:
                    states.append(row)


                list_alert = [x for x in states if x[0] == 'Alert']
                list_active = [x for x in states if x[0] == 'Active']
                list_qop = [x for x in states if x[0] == 'QOP']
                list_qhh = [x for x in states if x[0] == 'QHH']
                list_sws = [x for x in states if x[0] == 'SWS-like']
                list_rem = [x for x in states if x[0] == 'REM-like']
                list_oem = [x for x in states if x[0] == 'OEM']

            for s in list_alert:
                with open(ulib.path_data['processed']+'durations_alert_'+f, mode='w', newline='') as csvfile:
                    result_interval_file = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    result_interval_file.writerow([ulib.get_interval_in_seconds(s[1],s[2])])

            for s in list_active:
                with open(ulib.path_data['processed']+'durations_active_'+f, mode='w', newline='') as csvfile:
                    result_interval_file = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    result_interval_file.writerow([ulib.get_interval_in_seconds(s[1],s[2])])

            for s in list_qop:
                with open(ulib.path_data['processed']+'durations_qop_'+f, mode='w', newline='') as csvfile:
                    result_interval_file = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    result_interval_file.writerow([ulib.get_interval_in_seconds(s[1],s[2])])

            for s in list_qhh:
                with open(ulib.path_data['processed']+'durations_qhh_'+f, mode='w', newline='') as csvfile:
                    result_interval_file = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    result_interval_file.writerow([ulib.get_interval_in_seconds(s[1],s[2])])

            for s in list_sws:
                with open(ulib.path_data['processed']+'durations_sws_'+f, mode='w', newline='') as csvfile:
                    result_interval_file = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    result_interval_file.writerow([ulib.get_interval_in_seconds(s[1],s[2])])

            for s in list_rem:
                with open(ulib.path_data['processed']+'durations_rem_'+f, mode='w', newline='') as csvfile:
                    result_interval_file = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    result_interval_file.writerow([ulib.get_interval_in_seconds(s[1],s[2])])

            for s in list_oem:
                with open(ulib.path_data['processed']+'durations_oem_'+f, mode='w', newline='') as csvfile:
                    result_interval_file = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    result_interval_file.writerow([ulib.get_interval_in_seconds(s[1],s[2])])