import numpy as np
import pickle as pkl
import matplotlib.pyplot as plt
from sys import argv

script, datfile, outname = argv

with open(datfile, 'rb') as datin:

	CenterPots = pkl.load(datin)
	Pore_Axes  = pkl.load(datin)
print(CenterPots,Pore_Axes)
# Calculate mean and error

Final = []

Final.append(np.mean(CenterPots, axis=0))
Final.append(np.mean(CenterPots, axis=0) + np.std(CenterPots, axis=0))
Final.append(np.mean(CenterPots, axis=0) - np.std(CenterPots, axis=0))

# Plot Data

for i in range(0,len(Final),1):
        plt.plot(Pore_Axes[0],Final[i])
plt.title("TEST")
plt.xlabel('Pore-Axis (A)')
plt.ylabel('Potential (kT/e)')
plt.ylim(-20,10)
plt.savefig(outname,dpi=600)
