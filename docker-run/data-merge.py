'''Merges individual data files into one huge file and deletes rest

'''
from __future__ import division
import pandas as pd
import os
import re
SORTED_FILES = {}
LOAD_AVG_INTERVAL = 1
def process_file(dir,fname,df):
    files = SORTED_FILES[cont_name]
    f_idx = [i for i in range(len(files)) if files[i] == fname][0]
    if f_idx > LOAD_AVG_INTERVAL:
        files = files[f_idx-LOAD_AVG_INTERVAL:f_idx+1]
    else:
        files = files[0:f_idx+1]
    # Now files that are needed for loadavg calculation are in files
    load_ctr = 0.0
    for filename in files:
        with open("{}/{}".format(dir, fname), "r") as f:
            lines = f.readlines()
            headers = lines[0].split(',')
            procs_running_index = [i for i in range(len(headers)) if headers[i] == 'container_nr_running'][0]
            procs_uninterruptible_index = [i for i in range(len(headers)) if headers[i] == 'container_nr_uninterruptible'][0]
            procs_sleeping_index = [i for i in range(len(headers)) if headers[i] == 'container_nr_sleeping'][0]
            data = lines[-1].split(',')
            # print float(data[procs_running_index]) , float(data[procs_uninterruptible_index]), float(data[procs_sleeping_index])
            load_ctr += float(data[procs_running_index]) + float(data[procs_uninterruptible_index]) + float(data[procs_sleeping_index])

    if len(files) != 0:
        loadavg = load_ctr/len(files)
        # print loadavg
    else:
        loadavg = 0.0
    # print loadavg
    df['simulated_load_avg'] = loadavg
    return df 

if __name__ == '__main__':
    containers = [i for i in os.listdir('data') if not i.endswith('.csv')]
    containers = [i for i in containers if re.match('^cont\d{1,2}$',i) != None]
    for cont_name in containers:
        print 'Processing files for container - {}'.format(cont_name)
        DF = None
        firsttime = True
        if SORTED_FILES.has_key(cont_name)==False:
            SORTED_FILES[cont_name] = sorted(os.listdir('data/{}'.format(cont_name)))
        files = SORTED_FILES[cont_name]
        for filename in files:
            filepath = 'data/{}/{}'.format(cont_name,filename)
            df = pd.read_csv(filepath)
            # df = process_file(dir='data/{}'.format(cont_name),fname=filename,df=df)
            if firsttime:
                firsttime = False
                DF = df    
            DF = DF.append(df)
        DF.to_csv('data/{}.csv'.format(cont_name))



