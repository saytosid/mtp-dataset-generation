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
                row.append(str(under_oom))

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
    titles.append('cpu_time_user')
    titles.append('cpu_time_system')
    titles.append('cpu_time_children_user')
    titles.append('cpu_time_children_system')







    # titles.append('under_oom')

    top_output['Titles'] = titles
    process_obj = psutil.Process(pid=pid)


    timestamp = str(int(time.time()))
    procs = top_output['Processes']
    for row in procs:titles.append('mem_rss')
        row.append(timestamp)
        pid = row[1]
        # oom_score
        with open('/proc/{}/oom_score'.format(pid),'r') as f:
            oom_score = int(f.read())
            row.append(str(oom_score))
        # proc io_counters
        io_counters = P.io_counters()
        row.append(io_counters.read_count)
        row.append(io_counters.write_count)
        row.append(io_counters.read_bytes)
        row.append(io_counters.write_bytes)
        row.append(io_counters.read_chars)
        row.append(io_counters.write_chars)
        # proc number-of-file-descriptors
        row.append(p.num_fds())
        # proc number-context-switches, voluntary and involuntary
        row.append(p.num_ctx_switches().voluntary)
        row.append(p.num_ctx_switches().involuntary)
        # proc memory params full
        mem_obj = p.memory_full_info()
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
        row.append(p.num_threads())
        # proc cpu times
        cpu_time_obj = P.cpu_times()
        row.append(cpu_time_obj.user)
        row.append(cpu_time_obj.system)
        row.append(cpu_time_obj.children_user)
        row.append(cpu_time_obj.children_system)



        # #under_oom
        # with open('/sys/fs/cgroup/memory/docker/{}/memory.oom_control'.format(container.id),'r') as f:
        #     under_oom = f.readlines()[1].split()[1]
        #     row.append(str(under_oom))
    with open("data/{}/{}.csv".format(container.name, timestamp), 'wb') as f:
        f.write(",".join(top_output['Titles']))
        f.write('\n')
        for row in top_output['Processes']:
            f.write(",".join(row))
            f.write('\n')


def start_collection_all_containers(containers):
    while True:            row.append(str(under_oom))

        for container in containers:
            thread.start_new_thread(collect_container, (container,))
        time.sleep(1)


if __name__ == '__main__':
    containers = client.containers.list()
    print containers
    create_directories(containers)
    start_collection_all_containers(containers)
    # stop_all_containers()
