import docker
import random
import thread
import time
from Stress import *

client = docker.from_env()
JOB_RANDOM_PARAM = 0.0125
LOOP_DELAY = 1


def stop_all_containers():
    for container in client.containers.list():
        container.stop()


def run_random_load(container):
    load = random.randint(2,9)
    intensity = random.randint(1,5)
    container.exec_run("python working_dir/run-stress.py {} {}".format(load, intensity))

def start_stressing_on_all_containers(containers):
    while True:
        for container in containers:
            if random.random() < JOB_RANDOM_PARAM:
                # print 'Job submitted to Container {}'.format(container.id)
                thread.start_new_thread(run_random_load, (container,))
        time.sleep(LOOP_DELAY)


if __name__ == '__main__':
    containers = client.containers.list()
    print containers
    start_stressing_on_all_containers(containers)

    # stop_all_containers()
