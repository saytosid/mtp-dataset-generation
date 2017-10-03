import docker
import random
import thread
import time
import os

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
    titles.append('under_oom')
    top_output['Titles'] = titles

    timestamp = str(int(time.time()))
    procs = top_output['Processes']
    for row in procs:
        row.append(timestamp)
        pid = row[1]
        with open('/proc/{}/oom_score'.format(pid),'r') as f:
            oom_score = int(f.read())
            row.append(str(oom_score))
        with open('/sys/fs/cgroup/memory/docker/{}/memory.oom_control'.format(container.id),'r') as f:
            under_oom = f.readlines()[1].split()[1]
            row.append(str(under_oom))

    with open("data/{}/{}.csv".format(container.name, timestamp), 'wb') as f:
        f.write(",".join(top_output['Titles']))
        f.write('\n')
        for row in top_output['Processes']:
            f.write(",".join(row))
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
