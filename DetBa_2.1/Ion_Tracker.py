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
#		- Tracking	: first[BsA/BsB/Pc], second[BsA/BsB/Pc], third[BsA,BsB,Pc]
#
#			- The tracking will be filled based off a series of conditional statements that ensure that it correctly tracks a full permeation event. S.T. the Tracking
#			parameters reset when it returns to a previus section (e.g. 'first[BsA] -> second[Pc] -> third[BsA]' will reset the variables, and will not increase ION_PERM)
#

import	numpy as np
import	matplotlib.pylab as plt
from	tqdm import tqdm
from sklearn.linear_model import LinearRegression

class ION:

	def __init__(self):

		print("""

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
		""")

		self.BsA_upper	=	int(input("What is the upper boundary of the top bulk-solvent? "))
		self.BsA_lower	=	int(input("What is the lower boundary of the top bulk-solvent? "))
		self.BsB_upper	=	- self.BsA_lower
		self.BsB_lower	=	- self.BsA_upper
		self.Pc_lower	=	self.BsB_upper
		self.Pc_upper	=	self.BsA_lower
		self.first	=	"MT"	# MT means empty
		self.second	=	"MT"
		self.third	=	"MT"
		self.PosION_PERM	=	0
		self.NegION_PERM	=	0
		self.Tinit		=	"MT"
		self.Tfina 		=	"MT"

	def tracker(self, file_list, d_col, outname, lag_base):

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
		def Order_Assign(bin_now,timestep):
			if self.first == "MT":
				if bin_now == "Pc":
					pass
				else:
					self.first = bin_now
					self.Tinit = timestep
			elif self.first == "BsA":
				if self.second == "MT":
					self.second = bin_now if bin_now == "Pc" else RESET(bin_now,timestep)
				elif self.second == "Pc":
					if bin_now == "Pc":
						pass
					elif bin_now == "BsB":
						self.third = bin_now
						self.Tfina = timestep
					elif bin_now == "BsA":
						RESET(bin_now,timestep)
					else:
						print("There is a condition you are not accounting for: 1")
				else:
					print("There is a condition you are not accounting for: 2")
			elif self.first == "BsB":
				if self.second == "MT":
					self.second = bin_now if bin_now == "Pc" else RESET(bin_now,timestep)
				elif self.second == "Pc":
					if bin_now == "Pc":
						pass
					elif bin_now == "BsA":
						self.third = bin_now
						self.Tfina = timestep
					elif bin_now == "BsB":
						RESET(bin_now,timestep)
					else:
						print("There is a condition you are not accounting for: 3")
				else:
					print("There is a condition you are not accounting for: 4")
			else:
				print("self.first is %s" % self.first)
				print("bin_now = %s" % bin_now)
				print("There is a condition you are not accounting for: 5")

		def Perm_Check(bin_now,timestep):
			if	self.first == "BsA" and self.second == "Pc" and self.third == "BsB":
				self.NegION_PERM += 1
				dt = (self.Tfina - self.Tinit) * lag_base/1000
				#print(f"{self.Tfina} - {self.Tinit}")
				RESET(bin_now,timestep)
				return 1,-1,dt
			elif	self.first == "BsB" and self.second == "Pc" and self.third == "BsA":
				self.PosION_PERM += 1
				dt = (self.Tfina - self.Tinit) * lag_base/1000
				#print(f"{self.Tfina} - {self.Tinit}")
				RESET(bin_now,timestep)
				return 1,1,dt
			else:
				return 0,0,0

		def RESET(bin_now,timestep=0):
			self.first	= bin_now
			self.second	= "MT"
			self.third	= "MT"
			self.Tinit  = timestep
			self.Tfina  = "MT"
			return "MT"

	################################################################################################################################################################################################

		out_log	= str(outname) + "_TEMP.log"
		Log	= open(out_log, 'w')
		Log.write("frame\tdt\tfilename\tdirection (+/-)\n")
		for file in file_list:
			Data = open(file,'r')
			for line in Data:
				val = line.split()
				if float(val[d_col]) > self.BsA_upper or float(val[d_col]) < self.BsB_lower:
					pass
				else:
					bin_now 	= Which_Bin(float(val[d_col]))
					Order_Assign(bin_now,int(val[0]))
					check,direc,dt = Perm_Check(bin_now,int(val[0]))
					if check == True:
						Log.write(str(val[0])+'\t'+str(dt)+'\t'+str(file)+'\t'+str(direc)+'\n')
					else:
						pass
			RESET("MT")
		Log.write(f"There were a total of {self.NegION_PERM + self.PosION_PERM} ions that permeated.")
		Log.close()

def process(inname, lag_base):
	# The output of tracker has the ion passages organized by ion, however I need them organized by passage time.
	# Create a list of namedTuples from the contents of the infile
	infile = str(inname) + "_TEMP.log"
	outfile = str(inname) + "_Tracking.log"
	ions = []
	# constant to recover ns in time.
	b = 1000/lag_base
	with open(infile) as FILE:
		next(FILE)
		for line in FILE:
			val = line.split()
			if val[0] != 'There':
				ions.append([(float(val[0])/b),val[1],val[3]])
	ions.sort()
	with open(outfile, 'w') as Log:
		hold = 0
		timelist = []
		permlist = []
		Log.write('Time (ns)\tdt\tPermeations\n')
		for ion in ions:
			Log.write(f"{ion[0]}\t{ion[1]}\t{int(ion[2])+hold}\n")
			hold = int(ion[2]) + hold
			timelist.append(float(ion[0]))
			permlist.append(hold)
		# Now the data is in a more friendly plotable way.
		# Time to just generate the linear models for the entire simulation, and the final 20 ns
		perm = np.array(permlist)
		time = np.array(timelist)
		time = time.reshape(-1,1)
		current_tot = LinearRegression().fit(time, perm)
		r_sq = current_tot.score(time, perm)
		Log.write(f'Total Simulation -- Current: {current_tot.coef_ * 160} pA, R$^2$: {r_sq}\n')
		# Find the total length of the simulation, then only save entries in the
		# list that are within the last 20 ns
		stop = np.round(time[-1]) - 20
		for i in range(len(time)):
			if time[i] < stop:
				time = time.delete(time, i)
				perm = perm.delete(perm, i)
		current_l20 = LinearRegression().fit(time, perm)
		r_sq = current_l20.score(time, perm)
		Log.write(f'Last 20ns -- Current: {current_tot.coef_ * 160} pA, R$^2$: {r_sq}\n')
