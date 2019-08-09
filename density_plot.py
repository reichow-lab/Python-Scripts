##########################################################################
##	Plots a smoothed histogram based on a gaussian function		##
##									##
##	Portland State University					##
##	P.I.	: Steve Reichow						##
##	Author	: Matthew Veter						##
##########################################################################

#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
from sys import argv

script, data = argv

# List comprehension of the y-values within the dataset (pulled from column index 1)
y	=	[float(line.split()[1]) for line in open(data, 'r')]

density	=	gaussian_kde(y)

xs	=	np.linspace(-180.0,180.0,200)

density.covariance_factor	=	lambda : .25
density._compute_covariance()

plt.plot(xs, density(xs))
plt.show()
