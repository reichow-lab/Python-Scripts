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
z, mean 	=	[], []
with open(infile, 'r') as f:
    for line in f:
        z.append(line.split()[0])
        mean.append(line.split()[1])

z               =   np.asarray(map(float, z))
mean            =   np.asarray(map(float, mean))

# Creating the whole figure
fig	        =	figure()

# Creating the mean subplot
ax1		=	fig.add_subplot(111)

znew		=	np.linspace(z.min(),z.max(),100)

spl		=	make_interp_spline(z, mean, k=3)
mean_smooth	=	spl(znew)

ax1.plot(znew, mean_smooth, color='black')

xlabel("z axis of pore (Angstroms)")
ylabel("Free energy (kcal/mol)")
plt.ylim(-3,3)

black_patch	=	mpatches.Patch(color='black', label='cAMP')
ax1.legend(handles=[black_patch], loc=1)

plt.title(title)
plt.show()
