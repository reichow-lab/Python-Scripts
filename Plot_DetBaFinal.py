##########################################################################
##	Plotting the PMF with the error shaded in			##
##									##
##	Portland State University					##
##	P.I.	: Steve Reichow						##
##	Author	: Matthew Veter						##
##########################################################################

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline
from pylab import figure, show, legend, ylabel, xlabel
import matplotlib.patches as mpatches
from sys import argv

script, infile = argv

title		=	input("Title of the figure? ")

# Unloading the data file
z, mean, plus, minus	=	np.loadtxt(infile, delimiter=' ', unpack=True)

# Creating the whole figure
fig	=	figure()

# Creating the mean subplot
ax1		=	fig.add_subplot(111)

znew		=	np.linspace(z.min(),z.max(),100)

spl		=	make_interp_spline(z, mean, k=3)
mean_smooth	=	spl(znew)

ax1.plot(znew, mean_smooth, color='black')

# Creating the error subplot
ax2		=	fig.add_subplot(111)

ax2.fill_between(z, plus, minus, facecolor='pink')

xlabel("z axis of pore (Angstroms)")
ylabel("Free energy (kcal/mol)")
plt.ylim(-1,3)

black_patch	=	mpatches.Patch(color='black', label='Average')
pink_patch	=	mpatches.Patch(color='pink', label='SEM')
ax1.legend(handles=[black_patch, pink_patch], loc=1)

plt.title(title)
plt.show()
