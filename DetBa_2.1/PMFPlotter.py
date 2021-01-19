import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from glob import glob
from sys import argv

script, system, outname, palette = argv
RateList = glob(system+"*rate_final.txt_asym.txt")
PssList = glob(system+"*Pss_final.txt")
print(RateList,PssList)
# Final: [Pore] [PMF_Pss] [PMF_rate] [PMF_rate-Pss] [label]
# Final:   0        1         2            3           4
Final = [[],[],[],[],[]]
labels = ["rate","pss"]
elemC,convF = 1.60217662e-19,(1e-9/1e-12)

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
                Final[4].append(labels[1])
for i in range(len(Final[0])):
    Final[3].append(Final[2][i]-Final[1][i])

#plt.xlim(0,260)
#plt.ylim(0,250)
sns.set_palette(palette)
plt.title('PMF')
plt.xlabel("Pore Axis (A)")
plt.ylabel('Energy (Kcal/mol)')
sns.lineplot(data=Final, x=Final[0], y=Final[1])
plt.savefig(outname+"_PssPMF.png", dpi=400)
plt.title('Driving Potential')
plt.xlabel("Pore Axis (A)")
plt.ylabel('Energy (Kcal/mol)')
sns.lineplot(data=Final, x=Final[0], y=Final[2])
plt.savefig(outname+"_RatesPMF.png", dpi=400)
plt.title('Driving Potential - PMF')
plt.xlabel("Pore Axis (A)")
plt.ylabel('Energy (Kcal/mol)')
sns.lineplot(data=Final, x=Final[0], y=Final[3])
plt.savefig(outname+"_DiffPMF.png", dpi=400)
