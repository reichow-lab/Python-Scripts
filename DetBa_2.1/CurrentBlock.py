import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from glob import glob
from sys import argv
import pandas as pd
script, system, N = argv
FileList = glob(system+"*Tracking.log")
FileList.sort()
# Bins: bin_range   count
Bins = [[]]
for i in range(1,int(N)+1):
    Bins.append(i)
for FILE in FileList:
    Bins.append([])
    with open(FILE, 'r') as f:
        all_lines = f.read().splitlines()
    # find the final Time, and cal
    FinalTime = all_lines[-1].split()[0]
    for i in range(1,N+1):
        hold, count = 0, 0
        for line in all_lines:
            if line.split()[0] == "Time" or line.split()[0] == "Total" or line.split()[0] == "Last":
                pass
            elif float(line.split()[0]) > (i-1)*(FinalTime/N) and float(line.split()[0]) <= (i)*(FinalTime/N):
                count += (line.split()[2] - hold)
                hold = line.split()[2]
        Bins[i].append((count/(FinalTime/N))*160)
with open(system+"Block.txt", w) as out:
    for i in range(N):
        out.write(f"{Bins[0][i]}\t")
        for j in range(len(FileList)):
            if (j-1) == len(FileList):
                out.write(f"{Bins[j][i]}\n")
            else:
                out.write(f"{Bins[j][i]}\t")
