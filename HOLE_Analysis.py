import numpy as np
from glob import glob
from sys import argv
import pickle as pkl
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

# Parse inputs
parser = argparse.ArgumentParser()
parser.add_argument("-dat", dest = "datstring", action = "store")
parser.add_argument("-out", dest = "outname", action = "store", default = "OUTFILE")
parser.add_argument("-min", dest = "min", action = "store", default = "45")
parser.add_argument("-max", dest = "max", action = "store", default = "60")

args = parser.parse_args()

# Create list of the appropriate HOLE files

hole_file_list = glob(args.datstring)
hole_file_list.sort()

# Load HOLE output files
up_lim  = 75
low_lim = -75
Pore_Radii = []
Pore_Axis  = np.arange(-75,76)
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
# define pore-region of interest, and record the averages through time.
# Pore_UpVsLow: [[Time (ns)],[Upper Avg],[Lower Avg]]
Pore_UpVsLow = [[],[],[]]
for i in range(h):
    for j in range(len(Pore_Radii_Time[0])):
        # separate the two halves of the channel.
        if Pore_Radii_Time[2] == i and Pore_Radii_Time[0] <= args.max and Pore_Radii_Time[0] >= args.min:
            hold_upper.append(Pore_Radii_Time[1])
        elif Pore_Radii_Time[2] == i and Pore_Radii_Time[0] >= (-1*args.max) and Pore_Radii_Time[0] <= (-1*args.min):
            hold_lower.append(Pore_Radii_Time[1])
    Pore_UpVsLow[0].append(h*10)
    Pore_UpVsLow[1].append(np.mean(hold_upper))
    Pore_UpVsLow[2].append(np.mean(hold_lower))
#fss Save Extracted data for future processing
with open(str(globstring + '_data.pkl'), 'wb') as out:
    pkl.dump(Pore_Radii, out)
    pkl.dump(Pore_Axis, out)
with open(str(globstring + '_Time.pkl'), 'wb') as out:
    pkl.dump(Pore_Radii_Time, out)
PoreRadiiDF = pd.DataFrame({"Pore Axis": Pore_Radii_Time[0], "Pore Radii": Pore_Radii_Time[1]})
PoreTimeDF  = pd.DataFrame({"Time (ns)": Pore_UpVsLow[0], "Upper Radii (Å)": Pore_UpVsLow[1], "Lower Radii (Å)": Pore_UpVsLow[2]})
plt.xlabel("Pore Axis")
plt.ylabel('Pore Radii')
sns.lineplot(data=PoreRadiiDF, x="Pore Axis", y="Pore Radii", hue=Pore_Radii_Time[2])
plt.savefig(args.outname+"_TTime.png", dpi=400)
plt.clf()
sns.lineplot(data=PoreTimeDF, x="Time (ns)", y="Upper Radii (Å)", palette=sns.color_palette(Reds_r, n_colors=1))
sns.lineplot(data=PoreTimeDF, x="Time (ns)", y="Lower Radii (Å)", palette=sns.color_palette(Blues_r, n_colors=1))
plt.savefig(args.outname+"_RTime.png", dpi=400)
plt.clf()
