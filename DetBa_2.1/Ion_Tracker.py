#!/usr/bin/python
#
#	Program	: Ion_Tracker.py
#	Author	: Bassam Haddad
#
#	This program seeks to count the number of ion permeation events that occur in an all-atom molecular dynamics (MD) simulation of Connexin gap junctions.
#	
#	This will be an experimental and new addition that will (hopefully) calculate the number of ion permeation events that satisfy the following scenario:
#	Given a Bulk_solvent_A (BsA), Protein_channel (Pc), and Bulk_solvent_B (BsB); A proper permeation event will occur if one of the following conditions are met on a per-ion-basis
#
#	1)	first[BsA]	second[Pc]	third[BsB]	fourth[N/A] 
#	2)	first[BsB]	second[Pc]	third[BsA]	fourth[N/A]
#	3)	first[BsA]	second[BsB]	third[Pc]	fourth[BsA]
#	4)	first[BsB]	second[BsA]	third[Pc]	fourth[BsB]
#	5)	first[Pc]	second[BsA]	third[BsB]	fourth[Pc]
#	6)	first[Pc]	second[BsB]	third[BsA]	fourth[Pc]
#
#	In the event that any of these conditions are met, then a variable 'ION_PERM' will change from 0 -> N, where N are the number of permeation events. If 'ION_PERM'
#	has a non-0 value, then it could be used to approximate a conductance value. (see Benoit Roux's 2004 review in Quarterly Reviews of Biophysics, equations 102 and 103.)
#
#
#	My plan is to make an ion class for each ion we are tracking, with attributes that keep track of where it is, and where it has been.
#
#	Parameters:
#
#		- Boundaries	: BsA, BsB, PC
#		- ION_PERM	: 0/N (where 'N' is a non-zero integer)
#		- Tracking	: first[BsA/BsB/Pc], second[BsA/BsB/Pc], third[BsA,BsB,Pc], fourth[BsA,BsB,Pc]
#
#			- The tracking will be filled based off a series of conditional statements that ensure that it correctly tracks a full permeation event. S.T. the Tracking 
#			parameters reset when it returns to a previus section (e.g. 'first[BsA] -> second[Pc] -> third[BsA]' will reset the variables, and will not increase ION_PERM)
#

import	numpy as np
import	matplotlib.pylab as plt
from	tqdm import tqdm

class ION:

	def __init__(self):

		print	""" 

				------------------ \n
				|    top bulk    | \n
				|	         | \n
				-----|      |----- \n
				     |      | 	   \n
				     | pore |	   \n
				     |      |	   \n
				-----|      |----- \n
				|	         | \n
				|   bottom bulk  | \n
				------------------ \n
		"""

		self.BsA_upper	=	int(raw_input("What is the upper boundary of the top bulk-solvent? "))

		self.BsA_lower	=	int(raw_input("What is the lower boundary of the top bulk-solvent? "))       

		self.BsB_upper	=	int(raw_input("What is the upper boundary of the bottom bulk-solvent? "))

		self.BsB_lower	=	int(raw_input("What is the lower boundary of the bottom bulk-solvent? "))

		self.Pc_lower	=	self.BsB_upper

		self.Pc_upper	=	self.BsA_lower

		self.first	=	"MT"	# MT means empty

		self.second	=	"MT"

		self.third	=	"MT"

		self.ION_PERM	=	0

	def tracker(self, num_ion, prefix, outname):

		""" The boundaries will remain immutable throughout the process of ion tracking, however the values self.first/second/third will be freely adjusted
		throughout the 'tracker' method. At the end of every loop, a conditional statement will check to see if any of the 4 conditions of permeation are met; if
		they are indeed met, then 'ION_PERM' will increase by 1."""	
	
	###############################################################################################################################################################################################
	#																							      #
	#											Tracker Functions										      #
	#																							      #
	###############################################################################################################################################################################################

		def Which_Bin(zcoord):

			if zcoord <= self.BsA_upper and zcoord > self.BsA_lower:

				bin_now	= "BsA"

			elif zcoord <= self.Pc_upper and zcoord >= self.Pc_lower:

				bin_now	= "Pc"

			elif zcoord < self.BsB_upper and zcoord >= self.BsB_lower:

				bin_now	= "BsB"

			return bin_now

		def Order_Assign(bin_now):

			if self.first == "MT":

				if bin_now == "Pc":

					pass

				else:

					self.first = bin_now

			elif self.first == "BsA":

				if self.second == "MT":

					self.second = bin_now if bin_now == "Pc" else RESET(bin_now)

				elif self.second == "Pc":

					if bin_now == "Pc":

						pass

					elif bin_now == "BsB":

						self.third = bin_now

					elif bin_now == "BsA":

						RESET(bin_now)

					else:

						print "There is a condition you are not accounting for: 1"

				else:

					print "There is a condition you are not accounting for: 2"

			elif self.first == "BsB":

				if self.second == "MT":

					self.second = bin_now if bin_now == "Pc" else RESET(bin_now)

				elif self.second == "Pc":

					if bin_now == "Pc":

						pass

					elif bin_now == "BsA":

						self.third = bin_now

					elif bin_now == "BsB":

						RESET(bin_now)

					else:

						print "There is a condition you are not accounting for: 3"

				else:

					print "There is a condition you are not accounting for: 4"

			else:
				
				print "self.first is %s" % self.first
				print "bin_now = %s" % bin_now
				print "There is a condition you are not accounting for: 5"
		
		def Perm_Check(bin_now):

			if	self.first == "BsA" and self.second == "Pc" and self.third == "BsB":

				self.ION_PERM += 1

				RESET(bin_now)

				return 1

			elif	self.first == "BsB" and self.second == "Pc" and self.third == "BsA":

				self.ION_PERM += 1

				RESET(bin_now)

				return 1

			else:

				return 0

		def RESET(bin_now):

			self.first	= bin_now

			self.second	= "MT"

			self.third	= "MT"

			return "MT"
	################################################################################################################################################################################################

		out_log	= str(outname) + "_Tracking.log"
		Log	= open(out_log, 'a')

		for c in tqdm(range(0,num_ion,1)):

			dat	= str(prefix) + str(c)

			Data	= open(dat)

			for line in Data:

				val = line.split()

				if float(val[1]) > self.BsA_upper or float(val[1]) < self.BsB_lower:

					pass

				else:

					bin_now 	= Which_Bin(float(val[1]))

					Order_Assign(bin_now)

					check = Perm_Check(bin_now)

					if check == True:

						Log.write(dat + '\n')

					else:
						pass

			RESET("MT")

		Log.write("There were a total of %s ions that permeated." % (self.ION_PERM))

		Log.close()	
