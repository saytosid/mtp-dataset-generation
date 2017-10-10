import docker
import random
import thread
import time
import os
import psutil
from gnlpy.cgroupstats import CgroupstatsClient

client = docker.from_env()
JOB_RANDOM_PARAM = 0.7
TIME_DELAY_JOBS_MIN = 3
TIME_DELAY_JOBS_MAX = 7


def stop_all_containers():
    for container in client.containers.list():
        container.stop()


def create_directories(containers):
    try:
        os.mkdir('data')
    except Exception as e:
        pass

    try:
        for container in containers:
            os.mkdir("data/" + container.name)
    except Exception as e:
        pass


def collect_container(container):
    top_output = container.top(ps_args='aux')
    # additional_data_add to top_output
    titles = top_output['Titles']
    titles.append('Timestamp')
    titles.append('OOM_Score')
    titles.append('io_read_count')
    titles.append('io_write_count')
    titles.append('io_read_bytes')
    titles.append('io_write_bytes')
    titles.append('io_read_chars')
    titles.append('io_write_chars')
    titles.append('num_fds')
    titles.append('num_ctx_switches_voluntary')
    titles.append('num_ctx_switches_involuntary')
    titles.append('mem_rss')
    titles.append('mem_vms')
    titles.append('mem_shared')
    titles.append('mem_text')
    titles.append('mem_lib')
    titles.append('mem_data')
    titles.append('mem_dirty')
    titles.append('mem_uss')
    titles.append('mem_pss')
    titles.append('mem_swap')
    titles.append('num_threads')
    titles.append('cpu_time_user')
    titles.append('cpu_time_system')
    titles.append('cpu_time_children_user')
    titles.append('cpu_time_children_system')
    # Container metrics
    titles.append('container_nr_sleeping')
    titles.append('container_nr_running')
    titles.append('container_nr_stopped')
    titles.append('container_nr_uninterruptible')
    titles.append('container_nr_iowait')
    titles.append('cpu_loadavg_simulated')
    titles.append('container_under_oom')

    top_output['Titles'] = titles
    timestamp = str(int(time.time()))
    procs = top_output['Processes']
    for row in procs:
        row.append(timestamp)
        pid = row[1]
        process_obj = psutil.Process(pid=int(pid))

        # oom_score
        with open('/proc/{}/oom_score'.format(pid), 'r') as f:
            oom_score = int(f.read())
            row.append(str(oom_score))
        # proc io_counters
        io_counters = process_obj.io_counters()
        row.append(io_counters.read_count)
        row.append(io_counters.write_count)
        row.append(io_counters.read_bytes)
        row.append(io_counters.write_bytes)
        row.append(io_counters.read_chars)
        row.append(io_counters.write_chars)
        # proc number-of-file-descriptors
        row.append(process_obj.num_fds())
        # proc number-context-switches, voluntary and involuntary
        row.append(process_obj.num_ctx_switches().voluntary)
        row.append(process_obj.num_ctx_switches().involuntary)
        # proc memory params full
        mem_obj = process_obj.memory_full_info()
        row.append(mem_obj.rss)
        row.append(mem_obj.vms)
        row.append(mem_obj.shared)
        row.append(mem_obj.text)
        row.append(mem_obj.lib)
        row.append(mem_obj.data)
        row.append(mem_obj.dirty)
        row.append(mem_obj.uss)
        row.append(mem_obj.pss)
        row.append(mem_obj.swap)
        # proc num_threads
        row.append(process_obj.num_threads())
        # proc cpu times
        cpu_time_obj = process_obj.cpu_times()
        row.append(cpu_time_obj.user)
        row.append(cpu_time_obj.system)
        row.append(cpu_time_obj.children_user)
        row.append(cpu_time_obj.children_system)

        # container level metrics
        c = CgroupstatsClient()
        cgrp_metrics_obj = c.get_cgroup_stats("/sys/fs/cgroup/cpu/docker/{}".format(container.id))
        row.append(cgrp_metrics_obj.nr_sleeping)
        row.append(cgrp_metrics_obj.nr_running)
        row.append(cgrp_metrics_obj.nr_stopped)
        row.append(cgrp_metrics_obj.nr_uninterruptible)
        row.append(cgrp_metrics_obj.nr_iowait)

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

        # under_oom
        with open('/sys/fs/cgroup/memory/docker/{}/memory.oom_control'.format(container.id), 'r') as f:
            under_oom = f.readlines()[1].split()[1]
            row.append(str(under_oom))

    with open("data/{}/{}.csv".format(container.name, timestamp), 'wb') as f:
        f.write(",".join(top_output['Titles']))
        f.write('\n')
        for row in top_output['Processes']:
            f.write(",".join([str(item) for item in row]))
            f.write('\n')


def start_collection_all_containers(containers):
    while True:
        for container in containers:
            thread.start_new_thread(collect_container, (container,))

        time.sleep(1)


if __name__ == '__main__':
    containers = client.containers.list()
    print containers
    create_directories(containers)
    start_collection_all_containers(containers)
    # stop_all_containers()
