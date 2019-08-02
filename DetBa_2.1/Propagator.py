#!/usr/bin/python
#
#	Program	: Propogator.py
#	Author	: Bassam Haddad
#
#	This program replaces both 'initiator.py' & 'continuator.py' from the previous iteration of DetBa_2.sh.
#	Propogator.py has two methods built into it:
#
#		- initialize	: Initializes matrix based off the needs of the user: len-by-len for rates-pmf, or len-by-2 for histograms.
#
#			Inputs	: Bin_init, Bin_fina, Bin_size, Array_dimensions
#			Outputs	: Initialized matrix, log_file containing the input information, and the number of bins
#
#
#		- populate 	: Populates the previously created matrix
#
#			Inputs	: Initialized matrix, numfiles, file-prefix
#			Outputs	: Populated matrix
#

import matplotlib.pylab as plt
import numpy as np
from tqdm import tqdm

# Initializes matrix for subsequent calculations. MxN matrix, such that M is number of bins (num_bins) long, and either 2 or num_bins wide. The N=2 matrix is for simple histograms, and the N=num_bins matrix is for transition matrices.

def initialize(bin_init, bin_fina, bin_size, outname, array_dim):

	out_log		=	str(outname) + ".log"		
	L		=	open(out_log, 'w')

	matrix_length	=	int(abs(bin_init) + abs(bin_fina))

	num_bins	=	matrix_length/bin_size
	num_bins	=	int(num_bins)

	L.write('bin_init: ' + str(bin_init) + '\n' + 'bin_fina: ' + str(bin_fina) + '\n' + 'bin_size: ' + str(bin_size) + '\n' + 'num_bins: ' + str(num_bins))
	L.close()

	if array_dim == 0:

		population_matrix=np.zeros((num_bins,2))
		return population_matrix

	else:

		population_matrix=np.zeros((num_bins,num_bins))
		return population_matrix

# This method populates a transition matrix from 1D data (e.g. ion trajectories along z-coordinate) 

def populate(matrix, prefix, num_files, bin_fina, bin_s, num_bins, array_dim, d_col):

	# This function takes a z-coordinate from a text file, and locates which bin in the matrix it belongs to.

	def Which_Bin(zcoord):

		if zcoord < 0:

			found_bin = False

			neg = 1

			while found_bin == False:

				to = neg*(bin_s) - bin_fina	# The purpose of this statement is to allow for variable sized bins. Thus the zcoord must be located within a range,
				fro = to - bin_s		# the range is then associated with a particular bin. 'to' & 'fro' are the edges of the bin, this code cycles through
								# all of the available bins, and asks whether or not the zcoord is within it. 
				if (zcoord >= fro) and (zcoord <= to):

					found_bin = True	# This, and the next if-statement seem confusing, but if you work it out on paper, it'll make sense.
					bin       = neg - 1

				else:

					found_bin = False
					neg       = neg + 1

		elif zcoord >= 0:

			found_bin = False

			pos = (num_bins/2) + 1

			while found_bin == False:

				to = pos*(bin_s) - bin_fina
				fro = to - bin_s

				if (zcoord >= fro) and (zcoord <= to):

					found_bin = True
					bin       = pos - 1

				else:

					found_bin = False
					pos       = pos + 1

		return bin

	def Populator(bin_then, bin_now):

		matrix[bin_then,bin_now] = matrix[bin_then,bin_now] + 1

		return 0


	def hist_pop(bin_now):

		matrix[bin_now, 1] = matrix[bin_now,1] + 1

		return 0
	
	###################################################################

	bin_j	=	0

	for c in tqdm(range(0,num_files,1)):

		dat = str(prefix) + str(c)

		Data = open(dat)

		for line in Data:

			val = line.split()

			if abs(float(val[d_col])) > bin_fina:	# changing from val[1] to val[3] to accomodate for the "measure center" command in VMD

				pass

			else:

				bin_i = bin_j
				bin_j = Which_Bin(float(val[d_col]))
				
				if array_dim == 1:	# Rates calculation: choice == 'R'

					hold = Populator(bin_i, bin_j)	

				elif array_dim == 0:	# Histogram calculation: choice == 'H'

					hold = hist_pop(bin_j)
		
	return matrix
