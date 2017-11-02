'''Merges individual data files into one huge file and deletes rest
TBI - It is not made yet, to be implemented

'''


titles.append('cpu_loadavg_simulated')
# simulated loadavg: 1 min avg of running and uninterruptible processes

files = sorted([item for item in os.listdir("data/{}".format(container.name)) if item.endswith(".csv")])[-59:]
load_ctr = cgrp_metrics_obj.nr_running + cgrp_metrics_obj.nr_uninterruptible
for file in files:
    with open("data/{}/{}".format(container.name, file), "r") as f:
        lines = f.readlines()
        headers = lines[0].split(',')
        procs_running_index = [i for i in range(len(headers)) if headers[i] == 'container_nr_running'][0]
        procs_uninterruptible_index = [i for i in range(len(headers)) if headers[i] == 'container_nr_uninterruptible'][0]
        data = lines[1].split(',')
        load_ctr += int(data[procs_running_index]) + int(data[procs_uninterruptible_index])
if len(files) != 0:
    loadavg = float(load_ctr) / len(files)
else:
    loadavg = 0.0
row.append(loadavg)
