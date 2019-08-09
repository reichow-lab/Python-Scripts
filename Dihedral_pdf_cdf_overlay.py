##########################################################################
##	Creation of a pdf/cdf from a dihedral angle dataset		##
##									##
##	Portland State University					##
##	P.I.	: Steve Reichow						##
##	Author	: Matthew Veter						##
##########################################################################

#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde as gkde
from pylab import figure, show, legend, ylabel, xlabel
from sys import argv

script, infile	=	argv

num_bins=	int(input("How many bins? "))
pdf_col	=	input("Color of the pdf? ")

# Unloading data file
x, y	=	np.loadtxt(infile, delimiter='\t', unpack=True)

# Creating the whole figure
fig1	=	figure()

# Creating the pdf subplot
ax1	=	fig1.add_subplot(111)
n, bins, patches	=	ax1.hist(y, num_bins, density=1, histtype='stepfilled', facecolor=pdf_col, alpha=0.5)

# Establishing the y-axis of the pdf and the x-axis
ylabel("Probability density")
plt.ylim(0, 0.025)
plt.xlim(-175,180)
plt.xticks(np.arange(-180,181, step=45))

# Overlaying the line of the pdf to give the edge definition
ax2	=	fig1.add_subplot(111, sharex=ax1, sharey=ax1, frameon=False)
#n2, bins2, patches2	=	ax2.hist(y, num_bins, density=1, histtype='step', color='black', alpha=0.5)

density	=	gkde(y)
xs	=	np.linspace(-180.0,180.0,360)

density.covariance_factor	=	lambda : 0.05
density._compute_covariance()

ax2.plot(xs, density(xs))

# Creating the cdf subplot
ax3	=	fig1.add_subplot(111, sharex=ax1, frameon=False)
ax3.hist(y, 1440, density=1, color='navy', histtype='step', cumulative=True)

# Establishing the y-axis of the cdf
ax3.yaxis.tick_right()
ax3.yaxis.set_label_position("right")
xlabel("Dihedral angle (degrees)")
ylabel("Cumulative density")

# Creating shared traits and the figure
plt.title("Frequency of glycosidic bond dihedral angles on cAMP in Cx46")
plt.show()
