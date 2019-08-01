#!/usr/bin/python

from sys import argv
from math import sqrt

script, SMD = argv

# Setting initial variables
outfile	=	raw_input("Name the output file: ")
num_lin	=	len(open(SMD).readlines())
data	=	open(SMD, 'r')
outf	=	open(outfile, 'w')
init = 0
delta_s	=	[]
force	=	[]

# Looping through timesteps to populate lists of force and change in position
# Commented out sections will give the 3-d trajectory of change in position. Irrelevant while using colvars
for line in data:

	val	=	line.split()

	if init == 0:

		#x_init	=	float(val[2])
		#y_init	=	float(val[3])
		z_init	=	float(val[4])
		force.append(float(val[7]))
		init 	+=	1

	else:

		#delta_x	=	float(val[2]) - x_init
		#delta_y	=	float(val[3]) - y_init
		delta_z	=	float(val[4]) - z_init
		#delta_s.append(sqrt((delta_x)**2 + (delta_y)**2 + (delta_z)**2))
		delta_s.append(delta_z)

		if  init < num_lin+1:

			#x_init	=	float(val[2])
			#y_init	=	float(val[3])
			z_init	=	float(val[4])
			force.append(float(val[7]))

		else:

			init	+=	1

s	=	[]
a	=	0

# Cumulates the change in position over the course of the trajectory
for n in delta_s:

	a	+=	n
	s.append(a)

# Writes the position and force to file in (x,y) format
for i,j in zip(s, force):

	outf.write(str(i) + '\t' + str(j) + '\n')

data.close()
outf.close()
