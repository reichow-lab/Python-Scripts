#!/usr/bin/python

##########################################################################################
##		Generates a smoothed line from a standard X,Y dataset			##
##											##
##	Portland State University							##
##	P.I.	: Steve Reichow								##
##	Author	: Bassam Haddad and Matthew Veter					##
##########################################################################################

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import splrep, splev
from sys import argv

script, data = argv

title = raw_input("What is the title of your graph: ")

xlab = raw_input("What is the label of the x-axis: ")
ylab = raw_input("What is the label of the y-axis: ")

f = open(data, 'r')

a, x, y = [], [], []

for line in f:

	a.append(line)

for line in a:

	val = line.split()

	x.append(float(val[0]))

	y.append(float(val[1]))

bspl	=	splrep(x,y, k=3)

x_smooth = np.linspace(min(x), max(x), 1000)

bspl_y	= splev(x_smooth, bspl)

plt.figure()
plt.plot(x_smooth, bspl_y, 'b')

#plt.plot(b,c)
plt.title(title)
plt.xlabel(xlab)
plt.ylabel(ylab)


plt.show()
