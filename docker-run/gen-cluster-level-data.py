import os
import pandas as pd
import numpy as np

CLUSTER_1 = []
CLUSTER_2 = []

if __name__ == '__main__':
	# cluster info
	with open('data/container_cluster_info') as f:
		lines = f.readlines()
		for line in lines:
			line = line.split('->')
			line = [i.strip() for i in line]
			if line[0] == 'CLUSTER_1':
				CLUSTER_1.append(line[1])
			if line[0] == 'CLUSTER_2':
				CLUSTER_2.append(line[1])
	
	# Merge cluster_1
	for cont in CLUSTER_1:
		
		with open('data/{}.csv'.format(cont)) as f:
			df = pd.read_csv(f,header=0)
			df.loc[:, ~df.columns.str.contains('^Unnamed')]
			cols = [col for col in df if not col.startswith('Unnamed:')]
			df = df[cols]
