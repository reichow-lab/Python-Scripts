
import numpy as np
from math import sqrt

Error	= {}			# Dictionary keeping track of which "cut_num" provides the smallest error

limit	= 70			# What the final PMF 'pore-axis' will be trimmed down to

#################################################################

def trim(PMF_in, cut_num, final=False):	# cut_num is the number of values from PMF_for[pore-axis] to cut.

	PMF_for		= [[],[]]               # Forward PMF, [[pore-axis],[PMF_for]]
	PMF_rev		= [[],[]]               # Reverse PMF, [[pore-axis],[PMF_rev]]

	with open(PMF_in, 'r') as data:

		for line in data:

			val	= line.split()

			PMF_for[0].append(float(val[0]))
			PMF_for[1].append(float(val[1]))

	for i in range(0,cut_num,1):			# This loop cuts the [pore-axis] accordingly, if cut_num == 0 then nothing happens

		del PMF_for[0][0]

	while len(PMF_for[0]) < len(PMF_for[1]):	# This ensures that the two sub-lists are the same length prior to trimming to the limit

		del PMF_for[1][-1]

	while PMF_for[0][0] < -limit:			# These two loops trim the PMF to the pre-defined limits

		del PMF_for[0][0]

		del PMF_for[1][0]

	while (PMF_for[0][-1] > limit) or (PMF_for[0][-1] == 0):

		del PMF_for[0][-1]

		del PMF_for[1][-1]


	PMF_rev[0]	=	PMF_for[0]		# Creates the PMF reverse PMF...same pore axis

	PMF_rev[1]	=	PMF_for[1][::-1]	# but reversed PMF values...the list slice [::-1] is reversing the second column

	#return PMF_for, PMF_rev, cut_num		# Putting this on hold, I am thinking of calling the error function from here directly instead of returning these PMF values

	PMF_avg		=	error(PMF_for, PMF_rev, cut_num)	# I don't actually need the new PMF at this point..once I find the optimal cut number, I'll call it later.

	if final == True:

		return PMF_avg

#################################################################

def error(PMF_for, PMF_rev, cut_num):

	PMF_avg		= [[],[],[]]	# Average PMF, [[pore-axis],[PMF_avg],[SEM]]. I am reassigning this everytime I call it to clear out the columns

	PMF_avg[0]	= PMF_for[0]

	hold            = np.zeros([1,2])

	for i in range(0,len(PMF_avg[0]),1):

		hold[0,0]	= PMF_for[1][i]

		hold[0,1]	= PMF_rev[1][i]

		PMF_avg[1].append(hold.mean())

		PMF_avg[2].append((hold.std())/sqrt(2))

	Error[cut_num] = sum(PMF_avg[2])

	print Error

	return PMF_avg

#################################################################

def final(PMF_avg):

	PMF_fin = [[],[],[],[]]         # Final PMF  , [[pore-axis],[PMF_avg_adj],[Avg+SEM],[Avg-SEM]]

	PMF_fin[0] 	= PMF_avg[0]

	for i in range(0,len(PMF_avg[0]),1):

		PMF_fin[1].append(PMF_avg[1][i] - PMF_avg[1][0])

		PMF_fin[2].append(PMF_fin[1][i] + PMF_avg[2][i])

		PMF_fin[3].append(PMF_fin[1][i] - PMF_avg[2][i])

	return PMF_fin

#################################################################
#								#
#			Main Program				#
#								#
#################################################################

def Prep(PMF_in, outname):

	CUT_NUMS = [0,1,2,3,4,5]	# Eventually I want to have it more dynamically search for cut nums, but just performing the calculation for all
					# of these cuts (usually it's around 3) and then finding the minimum should work well for now...
	for x in CUT_NUMS:

		trim(PMF_in, x)

	BESTCUT		= min(Error, key=Error.get)

	Average_PMF	= trim(PMF_in, BESTCUT, True)

	Final_PMF	= final(Average_PMF)

	with open(outname, "w") as ofile:

		for i in range(0,len(Final_PMF[0]),1):

			ofile.write(str(Final_PMF[0][i]) + " " + str(Final_PMF[1][i]) + " " + str(Final_PMF[2][i]) + " " + str(Final_PMF[3][i]) + "\n")


