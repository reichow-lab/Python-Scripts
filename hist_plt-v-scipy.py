#!/usr/bin/python

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from scipy.stats import gaussian_kde
from pylab import figure, show, legend, ylabel, xlabel
from sys import argv

script, data = argv


# List comprehension of the y-values within the dataset (pulled from column index 1)
y       =       [float(line.split()[1]) for line in open(data, 'r')]


# Create the whole figure
fig1	=	figure()


# Creating the scipy PDF subplot
ax1	=	fig1.add_subplot(111)

density =       gaussian_kde(y)

xs      =       np.linspace(-180.0,180.0,360)

density.covariance_factor       =       lambda : 0.05
density._compute_covariance()

ax1.plot(xs, density(xs))
ylabel("Probability density")
plt.ylim(0, 0.025)
plt.xlim(175,180)
plt.xticks(np.arange(-180,181, step=45))


# Creating the second subplot
ax2	=	fig1.add_subplot(111, sharex=ax1, frameon=False)

cdf	=	gaussian_kde.integrate_box_1d(density, -180.0, 180.0)

ax2.plot(cdf, 'r', label='cdf', linewidth=2)
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position("right")
xlabel("Dihedral angle (degrees)")
ylabel("Cumulative density")


# Plotting the figure
plt.show()
