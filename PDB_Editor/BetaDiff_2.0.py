#!/usr/bin/python

#################################################################################
#										#
#	Script will subtract the beta of pdb1 from the beta of pdb2		#
#	i.e. [New beta value]# = [pdb1 beta value] - [pdb2 beta value]		#
#										#
#	*pdb1 will provide all coordinates for resultant output file		#
#################################################################################

from sys import argv

script, pdb1, pdb2, ofile = argv

data1	=	open(pdb1, 'r')
data2	=	open(pdb2, 'r')
outf	=	open(ofile, 'a')

B1	=	[{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
B2	=	[{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
Bnew	=	[{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
Val0	=	[]
Val1	=	[]
Val2	=	[]
Val3	=	[]
Val4	=	[]
Val5	=	[]
Val6	=	[]
Val7	=	[]
Val8	=	[]
Val9	=	[]
Val10	=	[]
Val11	=	[]

# Pulling the beta values from each pdb into a dictionary assigned to their residue ID number based on its Chain ID
# e.g. {resid-1: beta-1, resid-2: beta-2, ... resid-n: beta-n}

for line in data2:

	val	=	line.split()

	if (str(val[0]) == 'ATOM') and (str(val[2]) == 'CA'):

		c		=	ord(val[4]) - 65	# turns the chain ID into an indexed value i.e. A = 0, B = 1, C = 2 etc..

		i		=	val[5]

		B2[c][i]	=	val[10]		# assigns the beta value to its residue ID within its chain

	else:
		pass

data2.close()

for line in data1:

	val	=	line.split()

	if (str(val[0]) == 'ATOM') and (str(val[2]) == 'CA'):

		c               =       ord(val[4]) - 65

		i		=	val[5]

		B1[c][i]	=	val[10]

	else:
		pass

data1.close()

# Combining the two lists together to simply subtract the values from eachother

for i in range(len(B1)):

	for key in B1[i]:

		if B2[i].has_key(key):

			Bnew[i][key]	=	[float(B1[i][key]) - float(B2[i][key])]

		else:
			Bnew[i][key]	=	0

# Pulling all the coordinate information from pdb1

data1	=	open(pdb1, 'r')

for line in data1:

	val	=	line.split()

	if (str(val[0]) == 'ATOM'):

		Val0.append(val[0])
		Val1.append(val[1])
		Val2.append(val[2])
		Val3.append(val[3])
		Val4.append(val[4])
		Val5.append(val[5])
		Val6.append(val[6])
		Val7.append(val[7])
		Val8.append(val[8])
		Val9.append(val[9])
		Val10.append(Bnew[ord(val[4]) - 65][val[5]])
		Val11.append(val[11])

# Taking all the parsed data and writing the new pdb file with new beta values

for i, j, k, l, m, n, o, p, q, r, s, t in zip(Val0, Val1, Val2, Val3, Val4, Val5, Val6, Val7, Val8, Val9, Val10, Val11):	# This format is very clever, I like it a lot! - BH

	if len(str(k)) == 3:

		 outf.write(str(i).ljust(6) + '' + str(j).rjust(5) + ' ' + str(k).rjust(4) + ' ' + str(l).ljust(3) + ' ' + str(m) + ' ' + str(n).rjust(3) + '     ' + str(o).rjust(7) + ' ' + str(p).rjust(7) + ' ' + str(q).rjust(7) + ' ' + str(r).rjust(5) + ' ' + str(s).ljust(5, '0') + '      ' + str(t) + '\n')

	else:

		outf.write(str(i).ljust(6) + '' + str(j).rjust(5) + ' ' + str(k).center(4) + ' ' + str(l).ljust(3) + ' ' + str(m) + ' ' + str(n).rjust(3) + '     ' + str(o).rjust(7) + ' ' + str(p).rjust(7) + ' ' + str(q).rjust(7) + ' ' + str(r).rjust(5) + ' ' + str(s).ljust(5, '0') + '      ' + str(t) + '\n')
outf.write(str('END' + '\n'))

outf.close()
data2.close()
data1.close()
