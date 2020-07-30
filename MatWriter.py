import numpy as np
from sys import argv

script, matfile, outname = argv

A = np.load(matfile, allow_pickle=True)

with open((str(outname) + '.txt'), 'w') as out:

	for i in range(0,len(A[0]),1):

		for j in range(0,len(A[1]),1):

			out.write(str(A[i][j]) + '\t')

		out.write('\n')
