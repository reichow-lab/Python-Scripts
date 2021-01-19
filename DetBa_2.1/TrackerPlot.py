import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from glob import glob
from sys import argv

script, system, start, outname, palette = argv

FileList = glob(system)
FileList.sort()
# Final: [time] [cum. permeations] [label] [hue] [Average Current]
Final = [[],[],[],[],[]]
labels, hues = [],[]
elemC,convF = 1.60217662e-19,(1e-9/1e-12)
for i in range(len(FileList)):
    hues.append(i)
    labels.append(input("Label? "))

for FILE,label,hue in zip(FileList,labels,hues):
    with open(FILE, 'r') as file:
        for line in file:
            val = line.split()
            if val[0] == "Time":
                pass
            elif val[0] == "Total" or val[0] == "Last":
                pass
            elif val[0] < start:
                pass
            else:
                Final[0].append(float(val[0]))
                Final[1].append(int(val[2]))
                Final[2].append(str(label))
                Final[3].append(int(hue))
                pA = (int(val[2])*elemC)/(float(val[0])*1e-9)/(1e-12)
                Final[4].append(pA)
plt.xlim(0,260)
plt.ylim(0,250)
sns.set_palette(palette, 4)
plt.title(input("Title? "))
plt.xlabel("Time (ns)")
plt.ylabel('<Current> (pA)')
sns.scatterplot(data=Final, x=Final[0], y=Final[4], hue=Final[2], edgecolor="none")
plt.savefig(outname+".png", dpi=400)
