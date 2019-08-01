##########################################################################
##	Creation of a pdf/cdf from a dataset				##
##									##
##	Portland State University					##
##	P.I.	: Steve Reichow						##
##	Author	: Matthew Veter						##
##########################################################################

#!/usr/bin/python

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from pylab import figure, show, legend, ylabel, xlabel
from sys import argv

script, infile	=	argv

# Unloading data file
x, y	=	np.loadtxt(infile, delimiter='\t', unpack=True)

# Creating the whole figure
fig1	=	figure()

# Creating the pdf subplot
ax1	=	fig1.add_subplot(111)
n, bins, patches	=	ax1.hist(y, bins='auto', density=1, facecolor='aqua', alpha=0.5)

# Establishing the y-axis of the pdf and the x-axis
ylabel("Probability density")
plt.ylim(0, 0.025)
plt.xlim(-175,180)
plt.xticks(np.arange(-180,181, step=45))

# Overlaying the line of the pdf to give the edge definition
ax2	=	fig1.add_subplot(111)
n, bins, patches	=	ax2.hist(y, bins='auto', density=1, histtype='step', color='black', alpha=0.5)

# Creating the cdf subplot
ax3	=	fig1.add_subplot(111, sharex=ax1, frameon=False)
ax3.hist(y, bins='auto', density=1, color='navy', histtype='step', cumulative=True)

# Establishing the y-axis of the cdf
ax3.yaxis.tick_right()
ax3.yaxis.set_label_position("right")
xlabel("Dihedral angle (degrees)")
ylabel("Cumulative density")

# Creating shared traits and the figure
plt.title("PDF and CDF of dihedral angles")
plt.show()
