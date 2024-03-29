#
#    Program: DetBa.py
#
#    The purpose of this program is to replace the current version DetBa_2.sh, a bash script that strung together a series of python scripts in an
#    ad-hoc fashion that was clunky, and potentially prone to error. This version will be entirely contained within this python program that uses the
#    aforementioned analysis scripts as modules.
#
#    initializer.py and continuator.py will be replaced by a singel program that does both jobs, since I can write a python conditional that can distinguish
#    between the first and not-first ion trajectories. This means that I will have to go into thos scripts (more likely create a new one) that creates functions that
#    can be called by this (DetBa.py) program.
#
#    This program should also make the original (DetBa.sh) script completely obsolete! The original script had a primitive binning mechanism that only allowed for rigid
#    1 A sized bins, which was re-done in DetBa_2 to allow for any bin size including sub angstrom bins, which proved useful calculating histograms for interatomic distances
#    an accidental feature of DetBa_2.sh that will be refined in this iteration.
#
#
#    Additions
#    _________
#
#    - Histogram_Builder    (1) -- working to make output in bins, and not angstroms. Or, if I am going to have angstroms, they should be accurate to the coarsed-graining.
#
#        - This option will allow one to create histograms of their data without creating excess rates based files
#          making the program 'Histobot' obsolete.
#        - Furthermore this will be the method used for creating distance based histograms. (see Myers, J.B. & Haddad, B.G. (Nature, 2018))
#        - Currently working on this, and almost finished, refer to README: 27-Sep-2018
#
#    - Ion_Counter         (1) -- Still testing. It seems to work, but then I feel it may overestimate in some cases.
#
#        - This will be an experimental and new addition that will (hopefully) calculate the number of ion permeation events that satisfy the following scenario:
#          Given a Bulk_solvent_A (BsA), Protein_channel (Pc), and Bulk_solvent_B (BsB); A proper permeation event will occur if one of the following conditions are met on a per-ion-basis
#            1)  ion goes from [BsA -> Pc] then from [Pc -> BsB] before [Pc -> BsA] occurs.
#            2)  ion goes from [BsB -> Pc] then from [Pc -> BsA] before [Pc -> BsB] occurs.
#            3)  ion goes from [Pc -> BsA] then from [BsA -> BsB] then [BsB -> Pc].
#            4)  ion goes from [Pc -> BsB] then from [BsB -> BsA] then [BsA -> Pc].
#          In the event that any of these conditions are met, then a variable 'ION_PERM' will change from 0 -> N, where N are the number of permeation events. If 'ION_PERM'
#          has a non-0 value, then it could be used to approximate a conductance value. (see Benoit Roux's 2004 review in Quarterly Reviews of Biophysics, equations 102 & 103.)
#
#    - PMF_Plotter        (0) -- In order for me to create this, I will either need it to 'clean-up' the data, or have Histogram_Builder clean up the data prior to plotting.
#
#        - This module would, neatly, plot the resulting PMFs with shaded in error-bars. This is a low priority, but a desired feature nontheless.
#
#    - Current_Calculator    (1)
#
#        - This module will use the formulation shown in Zonta et al. 2014, to calculate the mean first passage time (MFPT) of an ion traversing the PMF. Eventually this module will calculate the current given a voltage potential, and therefore an approximated I-V Curve.
#
#        - It will take a PMF, and Diffusion coefficient (which will eventually be calculated in this module), then use those to calculate the MFPT in either direction of the PMF... the current can be calculated as:
#
#            I = q(K_lr - K_rl)
#
#        Such that I is current, q is the charge of the particle and K is the rate constant calculated as (1/MFPT), the lr & rl subscripts denote left-right, and right-left.
#
#
#
#
#

import numpy as np
import matplotlib.pylab as plt
import Ion_Tracker
from Propagator import initialize,populate
from Calculator import sympop,rate2gibbs,hist_write,mfpt,check_SS
from Current_Calculator import Current,Text2PMF,VoltPMF
from Diffusion_Calc import normalize,Diff_Calc
from Edge_Erase import edge_erase,tri_diag
from PMF_Prep import Prep
from sys import argv
from glob import glob

script, globstring = argv

#################################
#                               #
#    Initial Variables          #
#                               #
#################################

file_list       =    glob(globstring)
bin_size        =    float(input("What is the desired bin size? "))
outname         =    str(input("What would you like to name this project? "))
choice          =    str(input("What would you like to do? MSM PMF (M), Histogram (H), Ion Tracker (T), I-V approximator (I) "))
choice          =    choice.upper()
out_pop_mat     =    outname + "_pop.mat"
out_rate_mat    =    outname + "_rate.mat"
out_IV          =    outname + "_I-V.data"
out_final       =    outname + "_Pss_final.txt"
lag_base        =    int(input("What is the step-size per frame? (answer in picoseconds) "))  # the base lag_time, or frame is 2ps...this can be softcoded later.

#################################
#                               #
#    Main Program               #
#                               #
#################################

END    =    False

while END == False:
    if choice == 'M':
        #het         =   bool(int(input("Homotypic (0), or Heterotypic (1)? ")))
        het         =   True
        d_col       =   int(input("Which column from your data_file will you use? "))
        lag_step    =   int(int(input(f"Choose a lag time. (multiple of {lag_base}ps) "))/lag_base)
        lag_time    =   lag_step * lag_base
        bin_lim     = input('What is the Bin limit? ') # "auto" is acceptable
        array_dim   =    1
        init_matrix,bin_min,bin_max,num_bins,ZtoBin,bin_dim = initialize(file_list, bin_size, outname, array_dim, d_col, bin_lim)
        first_center = bin_min + (bin_size/2)
        pop_matrix  =    populate(file_list, init_matrix, bin_min, bin_max, bin_size, num_bins, array_dim, d_col, lag_step, ZtoBin)
        #sym_matrix  =    sympop(bin_min, bin_size, pop_matrix, ZtoBin)
        #pop_matrix  = tri_diag(pop_matrix,bin_size)
        pop_matrix.dump(out_pop_mat)
        rate_matrix = normalize(pop_matrix)
        rate_matrix.dump(out_rate_mat)
        gibbs       =   rate2gibbs(num_bins, first_center, rate_matrix, bin_size, str(outname + '_rate'))
        Prep(gibbs, str(outname + '_rate_final.txt'), bin_dim, het)
        source      = int(input("Which bin is the source? "))
        sink        = int(input("which bin is the sink? "))
        gibbs,K_AB,MFPT,MSM,Pss =   mfpt(pop_matrix,num_bins,outname,source,sink,bin_min,bin_max,bin_size,ZtoBin,lag_time)
        Prep(gibbs, out_final, bin_dim, het)
        check_SS(MSM,Pss,num_bins,lag_time,outname,bin_size)
    elif choice == 'H':
        d_col       = int(input("Which column from your data_file will you use? "))
        array_dim   = 0
        lag_step    = 1
        bin_lim     = input('What is the Bin limit? ')
        init_matrix,bin_min,bin_max,num_bins,ZtoBin,bin_dim = initialize(file_list, bin_size, outname, array_dim, d_col, bin_lim)
        pop_matrix  =    populate(file_list, init_matrix, bin_min, bin_max, bin_size, num_bins, array_dim, d_col, lag_step, ZtoBin)
        write_mat    =    hist_write(bin_min, pop_matrix, outname, bin_size, num_bins)
    elif choice == 'T':
        d_col   =    int(input("Which column from your data_file will you use? "))
        ION        =    Ion_Tracker.ION()
        ION.tracker(file_list, d_col, outname, lag_base)
        Ion_Tracker.process(outname, lag_base)
    elif choice == 'A':
        ION        =    Ion_Tracker_DEV.ION()
        ION.tracker(num_files, prefix, outname)
    elif choice == 'I':
        PMF_txt = input("which PMF file would you like to use? ")
        PMF_0,num_bins  = Text2PMF(PMF_txt)
        pop_mat_EE      = edge_erase(np.load(out_pop_mat,allow_pickle=True),bin_size)
        trans_mat       = normalize(pop_mat_EE)
        Diff_pore       = Diff_Calc(trans_mat,bin_size)                         # Calculates in units (A^2/second)
        #print    "Diff_pore = %s" % Diff_pore
        Voltages        =    [-150,-100,-75,-50,-25,0,25,50,75,100,150]
        out            =    open(out_IV, 'w')
        out.write('dV (mV)' + ',' + 'Current (pA)' + ',' + 'Forward MFPT' + ',' + 'Reverse MFPT' + '\n')
        for V in Voltages:
            dV        =    float(V)
            pmf_v        =    VoltPMF(PMF_0,dV,num_bins)
            I,Tau_f,Tau_r    =    Current(pmf_v,num_bins,bin_size,Diff_pore)
            out.write(str(dV) + ',' + str(I) + ',' + str(Tau_f) + ',' + str(Tau_r) + '\n')
        out.close()
    choice        =    str(input("What would you like to do? MSM PMF (M), Histogram (H), Ion Tracker (T), I-V approximator (I), Exit (E) "))
    choice        =    choice.upper()
    if choice    ==    'E':
        END    =    True
    elif choice    in    {"M","H","T","I"}:
        END    =    False
        bin_size        =    float(input("What is the desired bin size? "))
    else:
        END    =    True
