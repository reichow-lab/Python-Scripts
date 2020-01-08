import os
from glob import glob

if os.path.isdir('./traj_segs/'):

	out		=	open(input('Outfile name: '), 'w')

	cwd		=	os.getcwd()

	PcoordList	=	glob(cwd+'/traj_segs/*/*/')

	for PcoordPath in PcoordList:

		os.chdir(PcoordPath)

		if os.path.isfile('pcoord.dat'):

			with open('pcoord.dat', 'r') as infile:

				for line in infile:

					val = line.split()

					out.write(val[0] + '\n' )
	out.close()

else:

	print('WE_Pcoord.py must be used in the working directory of the WE simulation.')
