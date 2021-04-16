import numpy as np
from glob import glob
from sys import argv
import pickle as pkl
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
script, globstring = argv

# Create list of the appropriate HOLE files

hole_file_list = glob(globstring)
hole_file_list.sort()

# Load HOLE output files
up_lim  = 65
low_lim = -65
Pore_Radii = []
Pore_Axis  = np.arange(-65,66)
Pore_Radii_Time = [[],[],[]]
print(len(hole_file_list))
# Extract relevant data from HOLE output files
h = 0
for hole_file in hole_file_list:
    with open(hole_file) as FileIN:
        temp_radii = []
        for line in FileIN:
            val = line.split()
            if (float(val[0]) <= up_lim and float(val[0]) >= low_lim):
                temp_radii.append(float(val[1]))
                Pore_Radii_Time[0].append(float(val[0]))
                Pore_Radii_Time[1].append(float(val[1]))
                Pore_Radii_Time[2].append(h)
        if len(temp_radii) > 0:
            Pore_Radii.append(temp_radii)
        h += 1
print(h)
# Save Extracted data for future processing
with open(str(globstring + '_data.pkl'), 'wb') as out:
    pkl.dump(Pore_Radii, out)
    pkl.dump(Pore_Axis, out)
with open(str(globstring + '_Time.pkl'), 'wb') as out:
    pkl.dump(Pore_Radii_Time, out)
PoreRadiiDF = pd.DataFrame({"Pore Axis": Pore_Radii_Time[0], "Pore Radii": Pore_Radii_Time[1]})
plt.xlabel("Pore Axis")
plt.ylabel('Pore Radii')
sns.lineplot(data=PoreRadiiDF, x="Pore Axis", y="Pore Radii", hue=Pore_Radii_Time[2], palette=sns.color_palette('Blues_r', n_colors = (h-1)))
plt.savefig(globstring+"_TEST.png", dpi=400)
plt.clf()
