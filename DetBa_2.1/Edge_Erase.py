#!/bin/python
#
#			Program	: Edge_Eraser.py
#			Author	: Bassam Haddad
#
#
#
#

import numpy as np

def edge_erase(pop_mat,bin_size=1,cutoff=10):

	"""
	Due to the periodic boundaries of a molecular simulation, one sees ion transition events going from the top of the box to the bottom of the box. When calculating transition
	probabilities, we find that there are some spurious probabilities for an ion moving "220" A in a single step (2 ps). This program takes the transition-population matrix and 
	erases the counts involving transitions across the periodic boundaries, which are manifested near the edges of the transition matrix which should be nearly diagonal.
	"""

	cutoff		= cutoff / bin_size

	num_row,num_col	= pop_mat.shape

	for i in range (0,num_row,1):

		for j in range(0,num_col,1):

			if abs(i - j) >= cutoff:

				pop_mat[i,j]	= 0

			else:

				pass
	return pop_mat
