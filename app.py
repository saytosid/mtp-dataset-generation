import os,sys,subprocess

class HiBenchInstance:
    def __init__(self,cpus=1,memory=1000,name='test'):
        self.cpus = cpus
        self.memory = memory
        self.docker_container_name = name
        try:
            self.runShellCmd('docker container stop {}'.format(self.docker_container_name)) # remove if existing
            self.runShellCmd('docker container rm {}'.format(self.docker_container_name)) # remove if existing
        except:
            pass
        
        cmd = 'docker run -t -d --name {} fno2010/hibench'.format(name) # create and run container
        self.runShellCmd(cmd)

    def doJob(self,jobID=0):
        # TBI
        pass
    
    def runInsideContainer(self,cmd):
        cmd = 'docker exec -t {} {}'.format(self.docker_container_name,cmd)
        return self.runShellCmd(cmd)

    def runShellCmd(self,cmd):
        cmd = cmd.split(' ')
        return subprocess.check_output(cmd)

    def stop(self):
        self.runShellCmd('docker container stop {}'.format(self.docker_container_name))

class MetricCollector:
    def __init__(self,hibench_instance):
        self.stop_signal = False
        # TBI

    def startCollection(self):
        while (self.stop_signal==False):
            self.collect()
        
    def stop(self):
        self.stop_signal = True

    def collect(self):
        # TBI
        pass
