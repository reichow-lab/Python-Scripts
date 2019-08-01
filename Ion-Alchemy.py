#usr/bin/python

#################################################################################
#										#
#            Transmutation of Ions for Seeded Sampling Simulations		#
#			Author:	Matthew Veter					#
#			Editor: Bassam Haddad					#
#################################################################################

from sys import argv
from sys import exit

script, infile = argv

ifile		=	open(infile, 'r')
psf		=	ifile.readline().split()[0]
pdb		=	ifile.readline().split()[0]
oprefix		=	str(raw_input('Set the prefix of your output file: '))
outnum		=	len(open(infile).readlines())-4
ifile.readline()
ion		=	[]

for i in range(outnum + 1):
	ion.append(ifile.readline().split())

ion.sort()

catmass		=	0
if ion[1][0] == "POT":
	catmass = 39.0983
elif ion[1][0] == "SOD":
	catmass = 22.9898

for i in range(outnum):

	inpsf	=	open(psf, 'r')

	with open(oprefix+str(i)+'.psf', 'a') as opsf:

		for line in inpsf:

			val = line.split()

			if len(line.strip()) > 0:

				if str(val[0]) == str(ion[i+1][4]):

					if val[3] == ion[i+1][0]:

						opsf.write(str(val[0]).rjust(8) + ' ' + str(val[1]).ljust(4) + ' ' + str(val[2]).ljust(4) + ' ' + str('CLA').ljust(4) + ' ' + str('CLA').ljust(4) + ' ' + str('CLA').ljust(4) + '  ' + str('-1.000000').rjust(9) + '      ' + str("35.4500").rjust(8) + '          ' + str(" 0") + '\n')

				elif str(val[0]) == str(ion[0][4]):

					if val[3] == ion[0][0]:

						opsf.write(str(val[0]).rjust(8) + ' ' + str(val[1]).ljust(4) + ' ' + str(val[2]).ljust(4) + ' ' + str(ion[i+1][0]).ljust(4) + ' ' + str(ion[i+1][0]).ljust(4) + ' ' + str(ion[i+1][0]).ljust(4) + '  ' + str('1.000000').rjust(9) + '      ' + str(catmass).rjust(8) + '          ' + str(" 0") + '\n')

				else:
					opsf.write(line)

			else:
				opsf.write(line)

	inpsf.close()

for i in range(outnum):

	inpdb	=	open(pdb, 'r')

	with open(oprefix+str(i)+'.pdb', 'a') as opdb:

		for line in inpdb:

			val	=	line.split()

			if len(val) > 2:

				if str(val[2]) == 'POT' or str(val[2]) == 'CLA' or str(val[2]) == 'SOD':

					v3      =       val[3]
					v4      =       val[4]
					v5      =       val[5]
					v11	=	val[11]

					if v3 == ion[i+1][0] and v4 == ion[i+1][2] and v5 == ion[i+1][1]:

						opdb.write(str(val[0]).ljust(6) + '' + str(val[1]).rjust(5) + ' ' + str(ion[0][0]).rjust(4) + ' ' + str(ion[0][0]).ljust(3) + ' ' + str(ion[0][2]) + ' ' + str(val[5]).rjust(3) + '     ' + str(val[6]).rjust(7) + ' ' + str(val[7]).rjust(7) + ' ' + str(val[8]).rjust(7) + ' ' + str(val[9]).rjust(5) + ' ' + str(val[10]).rjust(5) + '      ' + str(val[11]) + '\n')

					elif v3 == ion[0][0] and v4 == ion[0][2] and v5 == ion[0][1] and v11 == ion[0][3]:

						opdb.write(str(val[0]).ljust(6) + '' + str(val[1]).rjust(5) + ' ' + str(ion[i+1][0]).rjust(4) + ' ' + str(ion[i+1][0]).ljust(3) + ' ' + str(ion[i+1][2]) + ' ' + str(val[5]).rjust(3) + '     ' + str(val[6]).rjust(7) + ' ' + str(val[7]).rjust(7) + ' ' + str(val[8]).rjust(7) + ' ' + str(val[9]).rjust(5) + ' ' + str(val[10]).rjust(5) + '      ' + str(val[11]) + '\n')

					else:
						opdb.write(line)

				else:
					opdb.write(line)
			else:
				opdb.write(line)

	inpdb.close()

inpsf.close()
inpdb.close()
