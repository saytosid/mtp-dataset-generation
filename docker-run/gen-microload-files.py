from Stress import *

file_creater = CreateFile()

for intensity in range(1,6):
	CreateFile.doStress(intensity=intensity,filename='intensity_{}'.format(intensity))