import numpy as np
from glob import glob
from sys import argv

script, globstring = argv

filelist = glob(globstring)
ioncount = []
for File in filelist:
	with open(File) as FileIN:
		for line in FileIN:
			val = line.split()
			ioncount.append(int(val[0]))
print(np.mean(ioncount))
