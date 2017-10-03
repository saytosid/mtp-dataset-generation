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
    with open("data/{}/{}.csv".format(container.name, str(int(time.time()))), 'wb') as f:
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
