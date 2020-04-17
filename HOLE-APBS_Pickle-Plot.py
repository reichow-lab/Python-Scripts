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

with open(exp, 'rb') as datin:

	experiment = pkl.load(datin)

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
