#!/usr/bin/python
#
#	Program	: Calculator.py
#	Author	: Bassam Haddad
#
#	This module replaces both 'pop2matrix.py', and 'rate2gibbs.py' from the previous iteration of DetBa_2.sh.
#	Calculator.py has three methods build into it:
#
#		- pop2rate	: Creates a rate-matrix, calculated from the population matrix; which was calculated in 'Propogator.py'
#
#			Inputs	: Initial bin (init), Final bin (fina), population matrix (counts), bin size (bin_size)
#			Outputs	: Rate Matrix (markov)
#
#
#		- rate2gibbs	: Uses values from the matrix matrix, and calculates the gibbs free energy for the transitions between bins.
#
#			Inputs 	: Initial bin (init), Final bin (fina), rates matrix (matrix), bin size (bin_size), output file (outname)
#			Outputs	: 'Free-Energy vs. Position'
#
#		- hist_write	:
#
#
#
#
#

import numpy as np
from tqdm import tqdm

def pop2rate(init, fina, counts, bin_size):

	bin_init = int(init)
	bin_fina = int(fina)
	bin_s	 = int(bin_size)

	counter  = 0

	num_bins = (abs(bin_fina) + abs(bin_init))/bin_s

	markov=np.zeros_like(counts)

	for i in tqdm(range(0,num_bins,1)):

		for j in range(0,num_bins,1):

			for c in range(0,num_bins,1):

				counter = counter + counts[i,c]

			if counter == 0:

				pass

			else:

				markov[i,j] = counts[i,j]/counter

				counter = 0

	return markov

def rate2gibbs(init, fina, matrix, bin_size, outname):

	bin_init = int(init)
	bin_fina = int(fina)
	bin_s    = int(bin_size)
	sum	 = 0

	num_bins = (abs(bin_fina) + abs(bin_init))/bin_s

	out_file = str(outname) + "_penult.dat"

	out	 = open(out_file, 'w')

	gibbs = np.zeros((num_bins,2))

	i = 0

	def det_bal(forw, rev):

		if forw == 0 or rev == 0:

			#print 'this check worked'
			#print forw, rev
			gibb = 0
		else:

			rel = forw/rev

			gibb = -0.00198588*310*np.log(rel)

		return gibb

	for j in tqdm(range(1,num_bins,1)):	# This loop is the first to populate the matrix[i,0] column. I need to incrememnt bin_init by bin_s instead of 1.

		forw	= matrix[i,j]
		rev	= matrix[j,i]

		gib	= det_bal(forw, rev)

		gibbs[i,0] = bin_init
		gibbs[i,1] = gib

		bin_init   = bin_init + bin_s
		i	   = i + 1

	for b in tqdm(range(0,num_bins,1)):

		sum = sum + gibbs[b,1]
		gibbs[b,1] = sum

	for c in range(0,num_bins,1):

		bin = gibbs[c,0]

		gib = gibbs[c,1]

		out.write(str(bin) + ' ' + str(gib) + ' ' + '\n')

	out.close()

	return out_file				# This allows PMF_Prep.py to take the name of the created text-file and use it as an input.

def hist_write(init, pop_matrix, outname, bin_size, num_bins):

	bin_init = int(init)
	counter = 0
	row_tot = 0

	num_bins = int(num_bins)

	outfile		= outname + '_hist.dat'

	out = open(outfile, 'w')

	for i in tqdm(range(0,num_bins,1)):

		val1	= bin_init

		val2	= pop_matrix[i,1]

		val_1	= str(val1)
		val_2	= str(val2)

		out.write(val_1 + ' ' + val_2 + '\n')

		bin_init = bin_init + bin_size
















