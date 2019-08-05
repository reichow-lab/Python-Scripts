#!/usr/bin/python

from sys import argv

script, pdb, ofile = argv

data	=	open(pdb, 'r')
outf	=	open(ofile, 'a')
i	=	2

for line in data:

	val	=	line.split()

	if ((str(val[0]) == 'ATOM' or str(val[0]) == 'HETATM')) and (str(val[4]) == 'A'):

		new_0	=	(val[0])
		new_1	=	(i)
		new_2	=	(val[2])
		new_3	=	(val[3])
		new_4	=	(val[4])
		new_5	=	(val[5])
		new_6   =       (val[6])
                new_7   =       (val[7])
                new_8   =       (val[8])
                new_9   =       (val[9])
                new_10  =       (val[10])
                new_11  =       (val[11])

		outf.write(str(new_0).ljust(6) + ' ' + str(new_1).rjust(4) + ' ' + str(new_2).center(4) + ' ' + str(new_3).ljust(3) + ' ' + str(new_4) + ' ' + str(new_5).rjust(3) + '     ' + str(new_6).rjust(7) + ' ' + str(new_7).rjust(7) + ' ' + str(new_8).rjust(7) + ' ' + str (new_9).rjust(5) + ' ' + str(new_10).rjust(5) + '           ' + str(new_11) + '\n')		

		i	+=	1

	elif (str(val[0]) == 'TER') and (str(val[3]) == 'A'):

                new_0   =       str(val[0])
                new_1   =       str(i)
                new_2   =       str(val[2])
                new_3   =       str(val[3])
                new_4   =       str(val[4])

		outf.write(str(new_0).ljust(6) + ' ' + str(new_1).rjust(4) + '      ' + str(new_2).ljust(3) + ' ' + str(new_3) + ' ' + str(new_4).rjust(3) + '\n')

		i	+=	1

	else:
		outf.write(line)
		

data.close()
outf.close()
