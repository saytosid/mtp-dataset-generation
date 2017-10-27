'''Runs a load(1-9) from Stress.py with specific Intensity(1-5)

USAGE:
`python run-stress <load_id> <intensity>`
<load_id> = 1-9
<intensity> = 1-5

'''
from Stress import *
import sys

if __name__ == '__main__':
	load_id = int(sys.argv[1])
	intensity = int(sys.argv[2])
	print loads[load_id-1].doStress(intensity)