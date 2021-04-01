import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.interpolate import interp1d
import sys
import argparse
from PMFPlotter import PMFPlotter
from TrackerPlot import TrackerPlot
# Parse inputs
parser = argparse.ArgumentParser()
parser.add_argument("-dat", dest = "datstring", action = "store")
parser.add_argument("-out", dest = "outname", action = "store", default = "OUTFILE")
parser.add_argument("-p", "--pmf", dest = "Pchoice", action = "store", type=bool, default = False)
parser.add_argument("-t", "--track", dest = "Tchoice", action = "store", type=bool, default = False)
parser.add_argument("-b", "--obs", dest = "Bchoice", action = "store", type=bool, default = False)
parser.add_argument("-bs", dest = "ObString", action = "store")
parser.add_argument("-ws", "--windowsize", dest = "WS", type=int, action = "store", default = 100)
parser.add_argument("-c", dest = "palette", action = "store", default = "Blues_r")
parser.add_argument("-lt", dest = "LastTime", action = "store", type=int, default = 1800)
parser.add_argument("-dc", dest = "d_col", action = "store", type=int, default = 1)

args = parser.parse_args()

def WatFluxTrack(system,start,outname,palette,WS,LT,d_col):
    WinS = int(WS)
    FileList = glob(system+"*WatFlux*")
    FileList.sort()
    # Final: [time] [instant Permeations] [cum. permeations] [label] [Average Flux]
    Final = [[],[],[],[],[],[]]
    labels = []
    for i in range(len(FileList)):
        labels.append(input("Label? "))
    for FILE, label in zip(FileList, labels):
        with open(FILE, 'r') as f:
            all_lines = f.read().splitlines()
        # extract pertinent water tracking
        for line in all_lines:
                if line.split()[0] == "Time(ns)":
                    pass
                else:
                    Final[0].append(line.split()[0])
                    Final[1].append(line.split()[1])
                    Final[3].append(label)
        # generate the cumulative flux
        # generate the cumulative permeations
        for i in range(len(Final[0])):
            if i == 0:
                Final[2].append(0)
                Final[4].append(0)
            else:
                Final[2].append(Final[2][i-1] + Final[1][i])
                Final[4].append(Final[2][i] / Final[0][i])
        # generate the running average of water flux
        for i in range(len(Final[0])):





if args.Pchoice == True:

    PMFPlotter(args.datstring,args.outname,args.palette)

if args.Tchoice == True:

    TrackerPlot(args.datstring,0,args.outname,args.palette,args.WS,args.Bchoice,args.LastTime,args.d_col,args.ObString)
