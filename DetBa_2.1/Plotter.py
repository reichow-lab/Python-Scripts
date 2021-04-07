import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from glob import glob
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
parser.add_argument("-w", "--water", dest = "Wchoice", action = "store", type=bool, default = False)
parser.add_argument("-wl", "--watlimit", dest = "watlim", action = "store", type=float, default = 60)
parser.add_argument("-b", "--obs", dest = "Bchoice", action = "store", type=bool, default = False)
parser.add_argument("-bs", dest = "ObString", action = "store")
parser.add_argument("-ws", "--windowsize", dest = "WS", type=int, action = "store", default = 100)
parser.add_argument("-c", dest = "palette", action = "store", default = "Blues_r")
parser.add_argument("-lt", dest = "LastTime", action = "store", type=int, default = 1800)
parser.add_argument("-dc", dest = "d_col", action = "store", type=int, default = 1)

args = parser.parse_args()

def WatFluxTrack(system,outname,palette,WS,LT,d_col,watlim):
    WinS = int(WS)
    FileList = glob(system+"*WatFlux*")
    FileList.sort()
    print(FileList)
    # Final[i]: [[time] [instant Permeations] [cum. permeations] [label] [Average Flux] [instant current]]
    Final  = [[[],[],[],[],[],[]],[[],[],[],[],[],[]],[[],[],[],[],[],[]],[[],[],[],[],[],[]],[[],[],[],[],[],[]]]
    WinAVG = [[[],[],[],[]],[[],[],[],[]],[[],[],[],[]],[[],[],[],[]],[[],[],[],[]]]
    labels = []
    for i in range(len(FileList)):
        labels.append(input("Label? "))
    for FILE, label in zip(FileList, labels):
        with open(FILE, 'r') as f:
            all_lines = f.read().splitlines()
        # extract pertinent water tracking
        for z in range(5):
            for line in all_lines:
                if line.split()[0] == "Time(ns)":
                    pass
                else:
                    Final[z][0].append(float(line.split()[0]))
                    Final[z][1].append(int(line.split()[d_col]))
                    Final[z][3].append(label)
            # generate the cumulative flux
            # generate the cumulative permeations
            for i in range(len(Final[z][0])):
                if i == 0:
                    Final[z][2].append(0)
                    Final[z][4].append(0)
                    Final[z][5].append(0)
                else:
                    Final[z][2].append(Final[z][2][i-1] + Final[z][1][i])                                       # cumulative water permeations
                    Final[z][4].append(Final[z][2][i] / Final[z][0][i])                                         # Running Average water flux
                    Final[z][5].append((Final[z][2][i] - Final[z][2][i-1])/(Final[z][0][i] - Final[z][0][i-1])) # Instantaneous water flux
            # Separate to calculate running-averages
            HoldSep = []
            for i in range(len(FileList)):
                HoldSep.append([])
            n = -1
            for i in range(len(Final[z][0])):
                if float(Final[z][0][i]) <= 0:
                    n += 1
                HoldSep[n].append(Final[z][5][i])
            # WinAVG: Time  Current  Hue  Label
            # Defined at the top, outside of the j-loop
            h = 0
            for n in HoldSep:
                for i in range(len(n)-WinS):
                    WinAVG[z][0].append(Final[z][0][i])
                    hold = []
                    for j in range(WinS):
                        hold.append(float(n[i+j]))
                    WinAVG[z][1].append(np.mean(hold))
                    WinAVG[z][2].append(h)
                    WinAVG[z][3].append(labels[h])
                h += 1
            with open(outname+f'_wa_{z}.txt', 'w') as out:
                for i in range(len(WinAVG[z][0])):
                    out.write(f"{WinAVG[z][0][i]}\t{WinAVG[z][1][i]}\t{WinAVG[z][2][i]}\n")

        CumPermeations  = [[],[],[]]
        CumAverage      = [[],[],[]]
        WindowAverage   = [[],[],[]]
        zables          = [" 45 Å"," 30 Å","  0 Å","-30 Å","-45 Å"]
        for z in range(5):
            for i in range(len(Final[0][0])):
                CumPermeations[0].append(Final[0][2][i])
                CumPermeations[1].append(Final[z][2][i])
                CumPermeations[2].append(zables[z])
                CumAverage[0].append(Final[0][4][i])
                CumAverage[1].append(Final[z][4][i])
                CumAverage[2].append(zables[z])
            for i in range(len(WinAVG[0][0])):
                WindowAverage[0].append(WinAVG[0][1][i])
                WindowAverage[1].append(WinAVG[z][1][i])
                WindowAverage[2].append(zables[z])
        print(CumPermeations)
        CumPermeations  = pd.DataFrame({"Time (ns)": CumPermeations[0], "Cumulative Permeations": CumPermeations[1], "Pore Height": CumPermeations[2]})
        CumAverage      = pd.DataFrame({"Time (ns)": CumAverage[0], "Cumulative Average": CumAverage[1], "Pore Height": CumAverage[2]})
        WindowAverage   = pd.DataFrame({"Time (ns)": WindowAverage[0], "Windowed Average Flux (ns^-1)": WindowAverage[1], "Pore Height": WindowAverage[2]})
        # Plot DataFrame
        plt.xlabel("Time (ns)")
        plt.ylabel('Windowed Avg. Water Flux (ns^-1)')
        sns.lineplot(data=WindowAverage, x="Time (ns)", y="Windowed Average Flux (ns^-1)", hue="Pore Height")
        plt.savefig(outname+"_WinWatFlux.png", dpi=400)
        plt.clf()
        sns.displot(data=WindowAverage, kind="kde")
        plt.xlim(-(args.watlim),args.watlim)
        plt.ylim(0,0.05)
        plt.savefig(outname+"_flux-hist.png", dpi=400)
        plt.clf()
        fig, ax = plt.subplots()
        plt.xlabel("Time (ns)")
        plt.ylabel('Cumulative Water Permeations')
        sns.scatterplot(data=CumPermeations, x="Time (ns)", y="Cumulative Permeations", edgecolor="none", hue="Pore Height")
        plt.savefig(outname+"_CumWaterPerm.png", dpi=400)
        plt.clf()
        fig, ax = plt.subplots()
        plt.xlabel("Time (ns)")
        plt.ylabel("Cumulative Avg. Water Flux (ns^-1)")
        sns.scatterplot(data=CumAverage, x="Time (ns)", y="Cumulative Average", edgecolor="none", hue="Pore Height")
        plt.savefig(outname+"_CumWaterFlux.png", dpi=400)
        plt.clf()



if args.Pchoice == True:

    PMFPlotter(args.datstring,args.outname,args.palette)

if args.Tchoice == True:

    TrackerPlot(args.datstring,0,args.outname,args.palette,args.WS,args.Bchoice,args.LastTime,args.d_col,args.ObString)

if args.Wchoice == True:

    WatFluxTrack(args.datstring,args.outname,args.palette,args.WS,args.LastTime,args.d_col,args.watlim)
