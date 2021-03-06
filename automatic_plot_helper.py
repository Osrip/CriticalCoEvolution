from os import listdir
from os.path import isfile, join
import os
import sys
import numpy as np
import pickle
import psutil
from pathlib import Path
import time
import warnings

def detect_all_isings(sim_name, type):
    '''
    Creates iter_list
    detects the ising generations in the isings folder
    '''
    curdir = os.getcwd()
    if type == 'pred':
        mypath = curdir + '/save/{}/pred_isings/'.format(sim_name)
    elif type == 'prey':
        mypath = curdir + '/save/{}/prey_isings/'.format(sim_name)

    all_isings = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith('isings.pickle')]
    gen_nums = []
    for name in all_isings:
        i_begin = name.find('[') + 1
        i_end = name.find(']')
        gen_nums.append(int(name[i_begin:i_end]))
    gen_nums = np.sort(gen_nums)
    return gen_nums

def load_settings(loadfile):
    '''
    load settings from loadfile
    :param loadfile: simulation name
    '''
    curdir = os.getcwd()
    load_settings = '/save/{}/settings.pickle'.format(loadfile)
    settings = pickle.load(open(curdir + load_settings, 'rb'))
    return settings

def load_isings(loadfile, type):
    '''
    Load all isings pickle files and return them as list
    :param loadfile : simulation name
    '''
    iter_list = detect_all_isings(loadfile, type)
    settings = load_settings(loadfile)

    isings_list = []
    for ii, iter in enumerate(iter_list):
        if type == 'pred':
            filename = 'save/' + loadfile + '/pred_isings/gen[' + str(iter) + ']-isings.pickle'
        elif type == 'prey':
            filename = 'save/' + loadfile + '/prey_isings/gen[' + str(iter) + ']-isings.pickle'

        startstr = 'Loading simulation:' + filename
        print(startstr)

        try:
            file = open(filename, 'rb')
            isings = pickle.load(file)
            file.close()
        except Exception:
            print("Error while loading %s. Skipped file" % filename)
            # Leads to the previous datapoint being drawn twice!!

        isings_list.append(isings)
    return isings_list

def load_isings_from_list(loadfile, iter_list):
    '''
    Load isings pickle files specified in iter_list and return them as list
    :param loadfile : simulation name
    :param iter_list : list of ints
    '''
    settings = load_settings(loadfile)
    numAgents = settings['pop_size']
    isings_list = []
    for ii, iter in enumerate(iter_list):
        filename = 'save/' + loadfile + '/isings/gen[' + str(iter) + ']-isings.pickle'
        startstr = 'Loading simulation:' + filename
        print(startstr)

        try:
            file = open(filename, 'rb')
            isings = pickle.load(file)
            file.close()
        except Exception:
            print("Error while loading %s. Skipped file" % filename)
            # Leads to the previous datapoint being drawn twice!!

        isings_list.append(isings)
    return isings_list

def list_to_blank_seperated_str(list):
    out_str = ''
    for en in list:
        out_str += str(en) + ' '
    out_str = out_str[:-1]
    return out_str

def wait_for_enough_memory(sim_name):
    '''
    Stops program until enough memory is available to load in all ising files
    '''

    root_directory = Path('save/{}/prey_isings'.format(sim_name))
    size_prey_isings_folder = sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())

    root_directory = Path('save/{}/pred_isings'.format(sim_name))
    size_pred_isings_folder = sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())

    size_isings_folder = size_pred_isings_folder + size_prey_isings_folder

    memory_data = psutil.virtual_memory()
    available_memory = memory_data.available
    total_system_memory = memory_data.active

    if total_system_memory < size_isings_folder:
        raise warnings.warn("Your system's memory is not sufficient to load in isings file. Attempting it anyways hoping for enough swap")
    else:
        waited_seconds = 0
        while available_memory < size_isings_folder:
            time.sleep(10)
            waited_seconds += 10
            if waited_seconds > 1200:
                warnings.warn('''After 20 minutes there is still not enough memory available for plotting,
                 trying to plot now anyways hoping for enough swap space.''')
                break