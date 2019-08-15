##########################################################################
##	Plot a polar figure of dihedral angle versus z-coord		##
##									##
##	Portland State University					##
##	P.I.	: Steve Reichow						##
##	Author	: Matthew Veter						##
##########################################################################
#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
from sys import argv

script, infile  =   argv


#   Import data from input (r can act as the z-coord of the channel pore)
#   Theta is required to be in radians for the polar plotter
r,theta	=       np.loadtxt(infile, delimiter='\t', unpack=True)
theta   =       np.pi/180. * theta

ax	=	plt.subplot(111, projection='polar')
ax.set_xticks(np.pi/180. * np.linspace(180, -180, 8, endpoint=False))
ax.set_yticklabels([200000,400000,600000,800000,1000000])
ax.set_rlabel_position(90.0)
ax.scatter(theta, r, c='lightskyblue', alpha=0.002)
#ax.grid(False)

#   For offsetting the origin
ax.set_rorigin(-200000)
#ax.set_theta_zero_location('W', offset=2000)


#   For confining to a sector
ax.set_thetamin(-180)
ax.set_thetamax(180)

plt.style.use('dark_background')
figname	=	input("Give your figure a prefix: ")
figname	=	figname + '.png'
plt.savefig(figname)
