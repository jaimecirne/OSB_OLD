import os
import csv
import time
from datetime import datetime, timedelta

path_data ={
    'raw': './raw_data/',
    'raw_all': './raw_data/all',
    'raw_part': './raw_data/withoutfeeding',
    'work_all': './data/all',
    'work_part': './data/withoutfeeding',
    'work': './data/',
    'processed': './processed_data/',
    'intervals': './processed_data/intervals/',
    'img':'./images/',
    'splited':'./processed_data/intervals/splited/',
    'byclass':'./processed_data/intervals/byclass/',
}

relabel_states ={
    'Alerta': 'Alert',
    'Ativo': 'Active',
    'Quieto': 'QOP',
    'AMMD': 'QHH',
    'AMME': 'QHH',
    'QMMD': 'QHH',
    'QMME': 'QHH',
    'QPC': 'SWS-like',
    'QPCMORE': 'Long SWS-like',
    'QPCLESS': 'Short SWS-like',
    'REM': 'REM-like',
    'REMD': 'OEM',
    'REME': 'OEM',
}

def get_interval_in_seconds(time_s: str, time_e: str) -> int:
    """[get 2 strings in formmat hh:mm:ss and return the interval between their in seconds(int)]
    
    Arguments:
        time_s {str} -- [String 'hh:mm:ss']
        time_e {str} -- [String 'hh:mm:ss']
    
    Returns:
        int -- [interval in seconds]
    """
    return get_duration_in_seconds(time_s, time_e)

def get_duration_in_seconds(time_s: str, time_e: str) -> int:
    """[get 2 strings in formmat hh:mm:ss and return the duration between their in seconds(int)]
    
    Arguments:
        time_s {str} -- [String 'hh:mm:ss']
        time_e {str} -- [String 'hh:mm:ss']
    
    Returns:
        int -- [duration in seconds]
    """
    
    hour_s = int(time_s.split(':')[0])
    minutes_s = int(time_s.split(':')[1])
    seconds_s = int(time_s.split(':')[2])
    hour_e = int(time_e.split(':')[0])
    minutes_e = int(time_e.split(':')[1])
    seconds_e = int(time_e.split(':')[2])
    return (hour_e-hour_s)*3600  + (minutes_e-minutes_s)*60 + seconds_e-seconds_s

def str_time_to_int_seconds(time_s: str) -> int:
    """
    :param time: a str holding time in hh:mm:ss format
    :returns: valeu in seconds about the string
    :reises: ErrorStringTimeFormat
    get a string in fotmmat hh:mm:ss and return value in seconds (int)
    """

    hour = int(time_s.split(':')[0])
    minutes = int(time_s.split(':')[1])
    seconds = int(time_s.split(':')[2])
    return hour*3600  + minutes*60 + seconds

def init_data():
    create_data_from_raw()
    print_error_time()

def print_error_time():
    """
    [check error start ands end between states]
    """
    for f in os.listdir(path_data['work']):
        if f.endswith(".csv"):
            last_time = []
            line = 0
            with open(path_data['work']+f, 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
                for row in spamreader:
                    if any(row):
                        line = line +1
                        if last_time  == []:
                            last_time = row
                        elif last_time[2] != row[1]:
                            print(f)
                            print(str(line))
                            print(last_time)
                            print(row)

                        last_time = row


def create_data_from_raw():
    """
    [Clean, relable states, standardize the sheets in the raw data and copy to the work data ]
    """
    tdelta = None
    less = False
    start_time = '05:50:00'
    FMT = '%H:%M:%S'
    for f in os.listdir(path_data['raw_all']):
        if f.endswith(".csv"):
            cleaning_states = []
            states_raw = []
            with open(path_data['raw_all']+f, 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
                for row in spamreader:
                    if any(row):
                        states_raw.append(row)

            #cleaning empty and duration columns
            for i, r in enumerate(states_raw):
                r = list(filter(lambda a: a != '', r))
                if len(r) > 3:
                    r.pop(1)
                states_raw[i] = r

            # removing consecutive equals states
            for s in states_raw:
                if len(cleaning_states) > 0 and s[0] == cleaning_states[-1][0]:
                    cleaning_states[-1][2] = s[2]
                else:
                    cleaning_states.append(s)

            # change old names states to new names
            for i in range(len(cleaning_states)):
                if cleaning_states[i][0] == 'QPC':
                    s1 = cleaning_states[i][1]
                    s2 = cleaning_states[i][2]
                    s1_time = datetime.strptime(s1, FMT)
                    s1_time = datetime.strptime(s1, FMT)
                    
                    tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
                    #
                    limit_deltatime = timedelta(minutes=6,seconds=51/60)

                    if tdelta < limit_deltatime:
                        cleaning_states[i][0] = relabel_states.get('QPCLESS', cleaning_states[i][0])
                    else:
                        cleaning_states[i][0] = relabel_states.get('QPCMORE', cleaning_states[i][0])
                else:
                    cleaning_states[i][0] = relabel_states.get(cleaning_states[i][0], cleaning_states[i][0])

            # standardize start time to 05:50
            part_file = int(f.split('-')[1].split('.csv')[0])

            if part_file < 2:
                s1 = cleaning_states[0][1]
                s1_time = datetime.strptime(s1, FMT)
                s2_time = datetime.strptime(start_time, FMT) 
                if s1_time <= s2_time:
                    tdelta = datetime.strptime(start_time, FMT) - datetime.strptime(s1, FMT)
                    less = False
                else:
                    tdelta = datetime.strptime(s1, FMT) - datetime.strptime(start_time, FMT)
                    less = True
            
            for i in range(len(cleaning_states)):
                s_time = datetime.strptime(cleaning_states[i][1], FMT)
                e_time = datetime.strptime(cleaning_states[i][2], FMT)

                if less:
                    tdelta_s = s_time - tdelta
                    tdelta_e = e_time - tdelta

                    cleaning_states[i][1] = tdelta_s.strftime(FMT)
                    cleaning_states[i][2] = tdelta_e.strftime(FMT)
                else:
                    tdelta_s = s_time + tdelta
                    tdelta_e = e_time + tdelta

                    cleaning_states[i][1] = tdelta_s.strftime(FMT)
                    cleaning_states[i][2] = tdelta_e.strftime(FMT)

            # save new csv to work
            with open(path_data['work_all']+f, mode='w', newline='') as csvfile:
                result_file = csv.writer(csvfile, delimiter=';', quotechar='|')
                for cs in cleaning_states:
                    result_file.writerow(cs)
    
    for f in os.listdir(path_data['raw_part']):
        if f.endswith(".csv"):
            cleaning_states = []
            states_raw = []
            with open(path_data['raw_part']+f, 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
                for row in spamreader:
                    if any(row):
                        states_raw.append(row)

            #cleaning empty and duration columns
            for i, r in enumerate(states_raw):
                r = list(filter(lambda a: a != '', r))
                if len(r) > 3:
                    r.pop(1)
                states_raw[i] = r

            # removing consecutive equals states
            for s in states_raw:
                if len(cleaning_states) > 0 and s[0] == cleaning_states[-1][0]:
                    cleaning_states[-1][2] = s[2]
                else:
                    cleaning_states.append(s)

            # change old names states to new names
            for i in range(len(cleaning_states)):
                if cleaning_states[i][0] == 'QPC':
                    s1 = cleaning_states[i][1]
                    s2 = cleaning_states[i][2]
                    s1_time = datetime.strptime(s1, FMT)
                    s1_time = datetime.strptime(s1, FMT)
                    
                    tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
                    limit_deltatime = timedelta(minutes=6,seconds=51/60)

                    if tdelta < limit_deltatime:
                        cleaning_states[i][0] = relabel_states.get('QPCLESS', cleaning_states[i][0])
                    else:
                        cleaning_states[i][0] = relabel_states.get('QPCMORE', cleaning_states[i][0])
                else:
                    cleaning_states[i][0] = relabel_states.get(cleaning_states[i][0], cleaning_states[i][0])

            # standardize start time to 05:50
            part_file = int(f.split('-')[1].split('.csv')[0])

            if part_file < 2:
                s1 = cleaning_states[0][1]
                s1_time = datetime.strptime(s1, FMT)
                s2_time = datetime.strptime(start_time, FMT) 
                if s1_time <= s2_time:
                    tdelta = datetime.strptime(start_time, FMT) - datetime.strptime(s1, FMT)
                    less = False
                else:
                    tdelta = datetime.strptime(s1, FMT) - datetime.strptime(start_time, FMT)
                    less = True
            
            for i in range(len(cleaning_states)):
                s_time = datetime.strptime(cleaning_states[i][1], FMT)
                e_time = datetime.strptime(cleaning_states[i][2], FMT)

                if less:
                    tdelta_s = s_time - tdelta
                    tdelta_e = e_time - tdelta

                    cleaning_states[i][1] = tdelta_s.strftime(FMT)
                    cleaning_states[i][2] = tdelta_e.strftime(FMT)
                else:
                    tdelta_s = s_time + tdelta
                    tdelta_e = e_time + tdelta

                    cleaning_states[i][1] = tdelta_s.strftime(FMT)
                    cleaning_states[i][2] = tdelta_e.strftime(FMT)

            # save new csv to work
            with open(path_data['work_part']+f, mode='w', newline='') as csvfile:
                result_file = csv.writer(csvfile, delimiter=';', quotechar='|')
                for cs in cleaning_states:
                    result_file.writerow(cs)
