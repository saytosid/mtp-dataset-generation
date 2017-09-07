import os,sys

class HiBenchInstance:
    def __init__(self,cpus=1,memory=1000):
        self.cpus = spus
        self.memory = memory
        self.docker_container = # TBI


    def doJob(self,jobID=0):
        # TBI
    

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