#!/usr/bin/python
#
#	Program: DetBa.py
#
#	The purpose of this program is to replace the current version DetBa_2.sh, a bash script that strung together a series of python scripts in an
#	ad-hoc fashion that was clunky, and potentially prone to error. This version will be entirely contained within this python program that uses the
#	aforementioned analysis scripts as modules.
#
#	initializer.py and continuator.py will be replaced by a singel program that does both jobs, since I can write a python conditional that can distinguish
#	between the first and not-first ion trajectories. This means that I will have to go into thos scripts (more likely create a new one) that creates functions that
#	can be called by this (DetBa.py) program.
#
#	This program should also make the original (DetBa.sh) script completely obsolete! The original script had a primitive binning mechanism that only allowed for rigid
#	1 A sized bins, which was re-done in DetBa_2 to allow for any bin size including sub angstrom bins, which proved useful calculating histograms for interatomic distances
#	an accidental feature of DetBa_2.sh that will be refined in this iteration.
#
#
#	Additions
#	_________
#
#	- Histogram_Builder	(1) -- working to make output in bins, and not angstroms. Or, if I am going to have angstroms, they should be accurate to the coarsed-graining.
#
#		- This option will allow one to create histograms of their data without creating excess rates based files
#		  making the program 'Histobot' obsolete.
#		- Furthermore this will be the method used for creating distance based histograms. (see Myers, J.B. & Haddad, B.G. (Nature, 2018))
#		- Currently working on this, and almost finished, refer to README: 27-Sep-2018
#
#	- Ion_Counter 		(1) -- Still testing. It seems to work, but then I feel it may overestimate in some cases.
#
#		- This will be an experimental and new addition that will (hopefully) calculate the number of ion permeation events that satisfy the following scenario:
#		  Given a Bulk_solvent_A (BsA), Protein_channel (Pc), and Bulk_solvent_B (BsB); A proper permeation event will occur if one of the following conditions are met on a per-ion-basis
#			1)  ion goes from [BsA -> Pc] then from [Pc -> BsB] before [Pc -> BsA] occurs.
#			2)  ion goes from [BsB -> Pc] then from [Pc -> BsA] before [Pc -> BsB] occurs.
#			3)  ion goes from [Pc -> BsA] then from [BsA -> BsB] then [BsB -> Pc].
#			4)  ion goes from [Pc -> BsB] then from [BsB -> BsA] then [BsA -> Pc].
#		  In the event that any of these conditions are met, then a variable 'ION_PERM' will change from 0 -> N, where N are the number of permeation events. If 'ION_PERM'
#		  has a non-0 value, then it could be used to approximate a conductance value. (see Benoit Roux's 2004 review in Quarterly Reviews of Biophysics, equations 102 & 103.)
#
#	- PMF_Plotter		(0) -- In order for me to create this, I will either need it to 'clean-up' the data, or have Histogram_Builder clean up the data prior to plotting.
#
#		- This module would, neatly, plot the resulting PMFs with shaded in error-bars. This is a low priority, but a desired feature nontheless.
#
#	- Current_Calculator	(1)
#
#		- This module will use the formulation shown in Zonta et al. 2014, to calculate the mean first passage time (MFPT) of an ion traversing the PMF. Eventually this module will calculate the current given a voltage potential, and therefore an approximated I-V Curve.
#
#		- It will take a PMF, and Diffusion coefficient (which will eventually be calculated in this module), then use those to calculate the MFPT in either direction of the PMF... the current can be calculated as:
#
#			I = q(K_lr - K_rl)
#
#		Such that I is current, q is the charge of the particle and K is the rate constant calculated as (1/MFPT), the lr & rl subscripts denote left-right, and right-left.
#
#
#
#
#

import numpy as np
import matplotlib.pylab as plt
import Ion_Tracker
from Propagator 	import initialize,populate
from Calculator 	import pop2rate,rate2gibbs,hist_write
from Current_Calculator import Current,Text2PMF,VoltPMF
from Diffusion_Calc	import normalize,Diff_Calc
from Edge_Erase		import edge_erase
from PMF_Prep		import Prep

#################################
#				#
#	Initial Variables	#
#				#
#################################

#num_files		=	int(raw_input("How many input files are there? "))
#
#init			=	int(raw_input("What is your initial bin? "))
#
#fina			=	int(raw_input("What is your final bin? "))
#
#bin_size		=	float(raw_input("What is the desired bin size? "))
#
#outname			=	str(raw_input("What would you like to name this project? "))
#
#choice			=	str(raw_input("What would you like to do? Rates PMF (R), Histogram (H), Ion Tracker (T), I-V approximator (I) "))
#choice			=	choice.upper()
#
#matrix_length		=	int(abs(init) + abs(fina))
#
#num_bins		=	matrix_length/bin_size
#num_bins		=	int(num_bins)
#
#out_pop_mat		=	outname + "_pop.mat"
#
#out_rate_mat		=	outname + "_rate.mat"
#
#out_IV			=	outname + "_I-V.data"
#
#out_final		=	outname + "_final.txt"
#################################
#				#
#	Main Program		#
#				#
#################################
def R(DP):

    out_pop_mat =       DP["outname"] + "_pop.mat"

    out_rate_mat    =   DP["outname"] + "_rate.mat"

    out_final   =       DP["outname"] + "_final.txt"

    array_dim	=	1

    init_matrix	=	initialize(DP["init"], DP["fina"], DP["bin_size"], DP["outname"], array_dim)

    pop_matrix	=	populate(init_matrix, DP["prefix"], DP["num_files"], DP["fina"], DP["bin_size"], DP["num_bins"], DP["array_dim"], DP["d_col"])

    pop_matrix.dump(out_pop_mat)

    rate_matrix	=	pop2rate(DP["init"], DP["fina"], DP["pop_matrix"], DP["bin_size"])

    rate_matrix.dump(out_rate_mat)

    gibbs		=	rate2gibbs(DP["init"], DP["fina"], rate_matrix, DP["bin_size"], DP["outname"])

    Final		=	Prep(gibbs, out_final)

def H(DP):

    array_dim	=	0

    init_matrix	=	initialize(DP["init"], DP["fina"], DP["bin_size"], DP["outname"], array_dim)

    pop_matrix	=	populate(init_matrix, DP["prefix"], DP["num_files"], DP["fina"], DP["bin_size"], DP["num_bins"], array_dim, DP["d_col"])

    write_mat	=	hist_write(DP["init"], pop_matrix, DP["outname"], DP["bin_size"], DP["num_bins"])

def T(DP):

    ION		=	Ion_Tracker.ION()

    ION.tracker(DP["num_files"], DP["prefix"], DP["outname"])

def A(DP):

    ION		=	Ion_Tracker_DEV.ION()

    ION.tracker(DP["num_files"], DP["prefix"], DP["outname"])

def I(DP):

    PMF_txt			=	out_final

    PMF_0,num_bins		=	Text2PMF(PMF_txt)

    pop_mat_EE		=	edge_erase(np.load(out_pop_mat),DP["bin_size"])

    trans_mat		=	normalize(pop_mat_EE)

    Diff_pore		=	Diff_Calc(trans_mat,DP["bin_size"])						# Calculates in units (A^2/second)

    Voltages		=	[-150,-100,-75,-50,-25,0,25,50,75,100,150]

    out_IV              =       DP["outname"] + "_I-V.dat"

    out			=	open(out_IV, 'w')

    out.write('dV (mV)' + ',' + 'Current (pA)' + ',' + 'Forward MFPT' + ',' + 'Reverse MFPT' + '\n')

    for V in Voltages:

        dV		=	float(V)

        pmf_v		=	VoltPMF(PMF_0,dV,num_bins)

    	I,Tau_f,Tau_r	=	Current(pmf_v,num_bins,DP["bin_size"],Diff_pore)

    	out.write(str(dV) + ',' + str(I) + ',' + str(Tau_f) + ',' + str(Tau_r) + '\n')

	out.close()
