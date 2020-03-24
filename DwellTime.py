#!/home/bassam/.conda/envs/base/bin/python
# DwellTime.py
# Bassam Haddad
# Reichow Lab

import	numpy	as	np
from	glob	import	glob
from	sys	import	argv

script, seltext, state_min, state_max, del_t, outname = argv
dt = float(del_t)
"""
Seltext		: is the string that you'll feed into glob to find all of the files that you would like to analyze
state_min	: lower range for the state
state_max	: upper range for the stete
dt		: time step in units nanoseconds (ns)
"""

filelist = glob(seltext)

# Generate list of frames in a given state

Dwell_Frames	= [[],[]]
All_Frames	= []
for FILE in filelist:

	with open(FILE) as FILEin:

		for line in FILEin:

			val = line.split()

			All_Frames.append(float(val[1]))

			if float(val[1]) >= float(state_min) and float(val[1]) <= float(state_max):

				Dwell_Frames[0].append(val[0])
				Dwell_Frames[1].append(val[1])

Dwell_Times	= []
hold		= 0

# Populate a list of dwell times. It is here that we can impose a filter if we want to define a dwell as more than 1 frame...it was decided to count 1-frame dwells as such.

for i in range(0,(len(Dwell_Frames[0])-1),1):

	if (int(Dwell_Frames[0][i+1]) - int(Dwell_Frames[0][i])) == 1:

		hold += 1

	else:

		Dwell_Times.append(hold)
		hold = 1

# Create array of the dwell times, and calculate statistics
DT_Array	= np.array(Dwell_Times)

m_dwell		= np.mean(DT_Array) * dt
t_dwell		= np.sum(DT_Array) * dt
s_dwell		= np.sqrt(np.var(DT_Array)) * dt
t_total         = np.sum(All_Frames) * dt
dwell_percent   = (t_dwell / t_total) * 100

print(f"Total dwell-time : {dwell_percent} %")
print(f"Mean dwell-time	 : {m_dwell} ns")
print(f"Std Deviation	 : {s_dwell} ns")

# Generate histogram of dwell-times and dist(HG - Arg)
DT_out		= open((outname + "_DT_hist.txt"), 'w')
AF_out		= open((outname + "_AF_hist.txt"), 'w')
log_out         = open((outname + "_log.txt"), 'w')

log_out.write("Total Dwell" + "\t" + "Mean Dwell" + "\t\t" + "Dwell StDev" + "\n")
log_out.write(str(t_dwell) + "\t\t" + str(m_dwell) + "\t" + str(s_dwell) + "\n")
log_out.write("Input Variables" + "\n")
log_out.write("glob String:" + "\t" + str(seltext) + "\n")
log_out.write("State_Min:" + "\t" + str(state_min) + "\n")
log_out.write("State_Max:" + "\t" + str(state_max) + "\n")
log_out.write("Time-Step:" + "\t" + str(del_t) + "\n")
log_out.write("OutName:" + "\t" + str(outname) + "\n")
log_out.close()

AF_Array	= np.array(All_Frames)

DT_hist		= np.histogram(DT_Array,bins=100)
AF_hist		= np.histogram(AF_Array,bins=100)

DT_list		= [[],[]]
DT_list[0]	= DT_hist[0].tolist()
DT_list[1]	= DT_hist[1].tolist()

AF_list		= [[],[]]
AF_list[0]	= AF_hist[0].tolist()
AF_list[1]	= AF_hist[1].tolist()

for i in range(0,len(DT_list[0]),1):
	DT_out.write(str(DT_list[1][i]) + "\t" + str(DT_list[0][i]) + "\n")
DT_out.close()

for i in range(0,len(AF_list[0]),1):
	AF_out.write(str(AF_list[1][i]) + "\t" + str(AF_list[0][i]) + "\n")
AF_out.close()


