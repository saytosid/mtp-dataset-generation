import docker
import random

NUM_CONTAINERS = 2
client = docker.from_env()


def create_containers():
    containers = [client.containers.run("saytosid/myubuntu", detach=True) for i in xrange(NUM_CONTAINERS)]
    return containers


def stop_all_containers():
    for container in client.containers.list():
        container.stop()


def run_random_load(container):
    c = random.randint(100)
    m = random.randint(100)
    t = random.randint(100)
    container.exec_run("stress -c {} -m {} -t {}".format(c, m, t))


if __name__ == '__main__':
    containers = create_containers()
    print containers
    run_random_load(containers[0])
    # stop_all_containers()
