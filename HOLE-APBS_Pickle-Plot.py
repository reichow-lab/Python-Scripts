import numpy as np
import pickle as pkl
import matplotlib.pyplot as plt
from sys import argv

script, datfile, outname, choice, exp, color = argv

# Set color scheme

Color_Options = {'red': ['firebrick','lightcoral','lightcoral'], 'blue': ['royalblue','skyblue','skyblue'],
		'green': ['olivedrab','palegreen','palegreen'], 'purple': ['rebeccapurple','mediumpurple','mediumpurple']}

Color_Scheme  = Color_Options[color]

with open(datfile, 'rb') as datin:

	CenterPots = pkl.load(datin)
	Pore_Axes  = pkl.load(datin)

# Calculate mean and error

Final = []

Final.append(np.mean(CenterPots, axis=0))
Final.append(np.mean(CenterPots, axis=0) + np.std(CenterPots, axis=0))
Final.append(np.mean(CenterPots, axis=0) - np.std(CenterPots, axis=0))

# Import Experimental data

with open(exp, 'rb') as datain:

	experiment = pkl.load(datain)
# Write out .txt file for Excel

with open((outname + '.txt'), 'w') as excelout:
	excelout.write('Pore-Axis\tExp\tMD\t+SEM\t-SEM\n')
	for i in range(0,len(Pore_Axes),1):
		excelout.write(str(Pore_Axes[i])+'\t'+str(experiment[0][i])+str(Final[0][i])+'\t'+str(Final[1][i])+'\t'+str(Final[2][i])+'\n')
	excelout.close()
# Plot Data

if choice == "apbs":

	for i in range(0,len(Final),1):
        	plt.plot(Pore_Axes,Final[i],color=Color_Scheme[i])
	plt.plot(Pore_Axes,experiment[0],color='black')
	plt.title(input("Title? "))
	plt.xlabel('Pore-Axis (A)')
	plt.ylabel('Potential (kT/e)')
	plt.ylim(-20,10)
	plt.savefig(outname,dpi=600)

elif choice == "hole":

	for i in range(0,len(Final),1):
		plt.plot(Pore_Axes,Final[i],color=Color_Scheme[i])
	plt.plot(Pore_Axes,experiment[0],color='black')
	plt.title(input("Title? "))
	plt.xlabel('Pore-Axis (A)')
	plt.ylabel('Pore Radii (A)')
	plt.ylim(0,15)
	plt.savefig(outname,dpi=600)
