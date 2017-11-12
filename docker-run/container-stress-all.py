import docker
import random
import thread
import time
from Stress import *

client = docker.from_env()
JOB_RANDOM_PARAM_MAX = 0.15
JOB_RANDOM_PARAM = 0.025
LOOP_DELAY = 1
CLUSTER_1 = []
CLUSTER_2 = []

def stop_all_containers():
    for container in client.containers.list():
        container.stop()


def run_random_load(container):
    if container in CLUSTER_1:
        load = random.randint(2,5)
        intensity = random.randint(1,5)
        num_jobs_in_container = len(container.top())
        JOB_RANDOM_PARAM = random.random()/float(num_jobs_in_container) + 0.01
        if random.random() < JOB_RANDOM_PARAM:
            container.exec_run("python working_dir/run-stress.py {} {}".format(load, intensity))

    if container in CLUSTER_2:
        load = random.randint(5,9)
        intensity = random.randint(1,5)
        num_jobs_in_container = len(container.top())
        JOB_RANDOM_PARAM = random.random()/float(num_jobs_in_container) + 0.01
        if random.random() < JOB_RANDOM_PARAM:
            container.exec_run("python working_dir/run-stress.py {} {}".format(load, intensity))

def start_stressing_on_all_containers(containers):
    while True:
        for container in containers:
            JOB_RANDOM_PARAM = random.random()*JOB_RANDOM_PARAM_MAX
            if random.random() < JOB_RANDOM_PARAM:
                # print 'Job submitted to Container {}'.format(container.id)
                thread.start_new_thread(run_random_load, (container,))
        time.sleep(LOOP_DELAY)


if __name__ == '__main__':
    containers = client.containers.list()
    print containers
    CLUSTER_1 = sorted(containers)[0:len(containers)/2]
    CLUSTER_2 = sorted(containers)[len(containers)/2:]
    os.system('rm data/container_cluster_info')
    for cont in CLUSTER_1:
        with open('data/container_cluster_info', 'ab') as f:
            f.write('CLUSTER_1 -> {}\n'.format(cont.name))
    for cont in CLUSTER_2:
        with open('data/container_cluster_info', 'ab') as f:
            f.write('CLUSTER_2 -> {}\n'.format(cont.name))
    start_stressing_on_all_containers(containers)

    # stop_all_containers()
