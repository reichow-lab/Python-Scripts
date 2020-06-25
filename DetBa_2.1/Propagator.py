#
#    Program    : Propogator.py
#    Author    : Bassam Haddad
#
#    This program replaces both 'initiator.py' & 'continuator.py' from the previous iteration of DetBa_2.sh.
#    Propogator.py has two methods built into it:
#
#        - initialize    : Initializes pop_mat based off the needs of the user: len-by-len for rates-pmf, or len-by-2 for histograms.
#
#            Inputs    : bin_min, bin_max, bin_size, Array_dimensions
#            Outputs    : Initialized pop_mat, log_file containing the input information, and the number of bins
#
#
#        - populate     : Populates the previously created pop_mat
#
#            Inputs    : Initialized pop_mat, numfiles, file-prefix
#            Outputs    : Populated pop_mat
#

import numpy as np
from tqdm import tqdm
import itertools as it

# Initializes pop_mat for subsequent calculations. MxN pop_mat, such that M is number of bins (num_bins) long, and either 2 or num_bins wide. The N=2 pop_mat is for simple histograms, and the N=num_bins pop_mat is for transition matrices.
# Additionally, initialize() creates a dictionary where the keys are the int(zcoord) and the values are the bin indeces.

def initialize(file_list, bin_size, outname, array_dim, d_col, bin_lim='auto'):
    bin_min = 0
    bin_max = 0
    if bin_lim == 'auto':
        for file in file_list:
            Data = open(file,'r')
            for line in Data:
                val = line.split()
                if float(val[d_col]) <= bin_min:
                    bin_min = int(float(val[d_col]))
                if float(val[d_col]) >= bin_max:
                    bin_max = int(float(val[d_col]))
        bin_dim = min(abs(bin_min),abs(bin_max))
    else:
        bin_dim = int(bin_lim)
    while bin_dim % bin_size != 0:
        bin_dim -= 1
    bin_min = bin_dim * -1
    bin_max = bin_dim
    print(f'bin_min = {bin_min}, bin_max = {bin_max}')
    pop_mat_length    =    int(abs(bin_min) + abs(bin_max))
    num_bins        =    pop_mat_length/bin_size
    num_bins        =    int(num_bins)

    # Create dictionary with int(zcoord) and bin_index

    ZtoBin  = {}
    bin     = 0
    counter = 1
    for z in range(bin_min,bin_max,1):
        ZtoBin[z] = bin
        if counter % bin_size == 0:
            bin += 1
            counter += 1
        else:
            counter += 1

    with open(str(outname + '.log'), 'w') as log:
        log.write('bin_min: ' + str(bin_min) + '\n' + 'bin_max: ' + str(bin_max) + '\n' + 'bin_size: ' + str(bin_size) + '\n' + 'num_bins: ' + str(num_bins))
    if array_dim == 0:
        pop_mat = np.zeros((num_bins,2))
        return pop_mat,bin_min,bin_max,num_bins,ZtoBin
    else:
        pop_mat = np.zeros((num_bins,num_bins))
        return pop_mat,bin_min,bin_max,num_bins,ZtoBin

# This method populates a transition pop_mat from 1D data (e.g. ion trajectories along z-coordinate)

def populate(file_list, pop_mat, bin_max, bin_s, num_bins, array_dim, d_col, lag_step, ZtoBin):

    # Deprecated: This function was replaced by the ZtoBin{} dictionary.
    # This function takes a z-coordinate from a text file, and locates which bin in the pop_mat it belongs to.

    def Which_Bin(zcoord):
        if zcoord < 0:
            found_bin    = False
            neg         = 1
            while found_bin == False:
                to = neg*(bin_s) - bin_max    # The purpose of this statement is to allow for variable sized bins. Thus the zcoord must be located within a range,
                fro = to - bin_s            # the range is then associated with a particular bin. 'to' & 'fro' are the edges of the bin, this code cycles through
                                            # all of the available bins, and asks whether or not the zcoord is within it.
                if (zcoord >= fro) and (zcoord <= to):
                    found_bin = True    # This, and the next if-statement seem confusing, but if you work it out on paper, it'll make sense.
                    bin       = neg - 1
                else:
                    found_bin = False
                    neg       = neg + 1
        elif zcoord >= 0:
            found_bin = False
            pos = (num_bins/2) + 1
            while found_bin == False:
                to = pos*(bin_s) - bin_max
                fro = to - bin_s
                if (zcoord >= fro) and (zcoord <= to):
                    found_bin = True
                    bin       = pos - 1
                else:
                    found_bin = False
                    pos       = pos + 1
        return int(bin)

    def Populator(bin_then, bin_now, num_bins):
        if abs(bin_now - bin_then) < (num_bins - 1):
            pop_mat[bin_now,bin_then] += 1
        elif bin_now - bin_then < 0:
            pop_mat[(num_bins - 1),bin_then] += 1
        elif bin_now - bin_then > 0:
            pop_mat[0,bin_then] += 1

    def hist_pop(bin_now):
        pop_mat[bin_now, 1] = pop_mat[bin_now,1] + 1
        return 0

#####################################
#                                    #
#            Main Program            #
#                                    #
#####################################

    bin_j    =    0
    for file in tqdm(file_list):
        Data = open(file,'r')
        for line in it.islice(Data,0,None,lag_step):
            val = line.split()
            if abs(float(val[d_col])) > bin_max:    # changing from val[1] to val[3] to accomodate for the "measure center" command in VMD
                pass
            else:
                bin_i = bin_j
                bin_j = ZtoBin[int(float(val[d_col]))]
                #bin_j = Which_Bin(float(val[d_col]))
                if array_dim == 1:    # Rates calculation: choice == 'R'
                    Populator(bin_i, bin_j, num_bins)
                elif array_dim == 0:    # Histogram calculation: choice == 'H'
                    hist_pop(bin_j)
    return pop_mat
