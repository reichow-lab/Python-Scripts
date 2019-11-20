#
#	Program:	process_ion.py
#	Author:		Bassam Haddad
#
#		It is not always possible to load MD simulation trajectories in a single VMD session, and is therefore not possible to
#	pull entire ion trajectories at once. For example, if there are 100 ions in the simulation, but I need to load the simulation in
#	two halves, then I will end up with 200 ion trajectory files. such that ion_firsthalf_13 and ion_secondhalf_13 are the same ion
#	but their trajectories are split into two separate files. This convention makes future applications of DetBa.py problematic
#	specifically the ability to track the permeation of a single ion. Thus it would help to have a 1 file per ion. This program does
#	just that, it appends the trajectories of the "second half" to the "first half" and adjusts the time value such that it is a
#	continuous process.
#
#	To run the program simply type:
#
#		$ process_ion.py xxxx
#
#	where 'xxxx' is the adjustment needed to make to the time column of the "second half" data ... for example, them time in
#	'ion_firsthalf_13' goes from 0 - 10000, and the time in 'ion_secondhalf_13' also goes from 0 - 10000, the slide amount (xxxx)
#	will be 10000, such that your resulting file, 'ion_total_13', goes from 0 - 20000.
#
#	The prefix refers to the string up to the number, using our prior examples, the prefix for 'ion_firsthalf_13' would be
#	'ion_firsthalf_'.

from tqdm	import tqdm
from sys        import argv
import os

script, slide_amount = argv

num_files               =       int(raw_input("How many input files are there? "))

prefix			=	str(raw_input("What is the prefix of the files you want to slide? "))

for c in tqdm(range(0,num_files,1)):

	dat = str(prefix) + str(c)

	Data = open(dat, 'r')

	new = 'temp_' + str(c)

	newD = open(new, 'w')

	for line in Data:

		values = line.split()

		pos = float(values[0]) + float(slide_amount)

		newD.write(str(pos) + ' ' + str(values[1]) + '\n')

	Data.close()
	newD.close()

prefix_init		=	str(raw_input("What is the prefix of the leading file? "))
prefix_new		=	str(raw_input("What is the prefix of your new file? "))

for n in tqdm(range(0,num_files,1)):

	outfile = str(prefix_init) + str(n)

	outnew	= str(prefix_new) + str(n)

	oldfile = str(prefix) + str(n)

	infile	= 'temp_' + str(n)

	fout	= open(outfile, 'a')

	fin	= open(infile, 'r')

	data	= fin.read()

	fin.close()

	fout.write(data)

	fout.close()

	os.rename(outfile, outnew)

	os.remove(infile)

	os.remove(oldfile)
