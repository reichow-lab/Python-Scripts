import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from glob import glob
from sys import argv
import pandas as pd

script, system, outname, palette = argv
RateList = glob(system+"*rate_final.txt_asym.txt")
PssList = glob(system+"*Pss_final.txt")
print(RateList,PssList)
# Final: [Pore] [PMF_Pss] [PMF_rate] [PMF_rate-Pss] [label]
# Final:   0        1         2            3           4
Final = [[],[],[],[],[]]
labels = ["all"]

for FILE in RateList:
    with open(FILE, 'r') as file:
        for line in file:
            val = line.split()
            if val[0] == "Pore":
                pass
            else:
                Final[0].append(float(val[0]))
                Final[2].append(float(val[1]))
                Final[4].append(labels[0])
for FILE in PssList:
    with open(FILE, 'r') as file:
        for line in file:
            val = line.split()
            if val[0] == "Pore":
                pass
            else:
                Final[1].append(float(val[1]))
for i in range(len(Final[0])):
    Final[3].append(Final[2][i]-Final[1][i])
print(len(Final[0]),len(Final[1]),len(Final[2]),len(Final[3]),len(Final[4]))
plot_data1 = pd.DataFrame({"Pore-Axis (A)":Final[0], "Energy (Kcal/mol)": Final[1]})
plot_data2 = pd.DataFrame({"Pore-Axis (A)":Final[0], "Energy (Kcal/mol)": Final[2]})
plot_data3 = pd.DataFrame({"Pore-Axis (A)":Final[0], "Energy (Kcal/mol)": Final[3]})
plt.xlim(-85,85)
plt.ylim(-0.5,3)
sns.set_palette(palette)
plt.title('PMF')
plt.xlabel("Pore Axis (A)")
plt.ylabel('Energy (Kcal/mol)')
sns.lineplot(data=plot_data1, x="Pore-Axis (A)", y="Energy (Kcal/mol)", hue=Final[4], style=Final[4])
plt.savefig(outname+"_PssPMF.png", dpi=400)
plt.clf()
plt.xlim(-85,85)
plt.ylim(-2,3.5)
plt.title('Driving Potential')
plt.xlabel("Pore Axis (A)")
plt.ylabel('Energy (Kcal/mol)')
sns.lineplot(data=plot_data2, x="Pore-Axis (A)", y="Energy (Kcal/mol)", hue=Final[4], style=Final[4])
plt.savefig(outname+"_RatesPMF.png", dpi=400)
plt.clf()
plt.xlim(-85,85)
plt.ylim(-2.5,2.5)
plt.title('Driving Potential - PMF')
plt.xlabel("Pore Axis (A)")
plt.ylabel('Energy (Kcal/mol)')
sns.lineplot(data=plot_data3, x="Pore-Axis (A)", y="Energy (Kcal/mol)", hue=Final[4], style=Final[4])
plt.savefig(outname+"_DiffPMF.png", dpi=400)
plt.clf()
