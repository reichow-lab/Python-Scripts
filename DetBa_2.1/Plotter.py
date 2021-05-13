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
from TrackerPlot import Interp
# Parse inputs
parser = argparse.ArgumentParser()
parser.add_argument("-dat", dest = "datstring", action = "store")
parser.add_argument("-out", dest = "outname", action = "store", default = "OUTFILE")
parser.add_argument("-p", "--pmf", dest = "Pchoice", action = "store", type=bool, default = False)
parser.add_argument("-t", "--track", dest = "Tchoice", action = "store", type=bool, default = False)
parser.add_argument("-w", "--water", dest = "Wchoice", action = "store", type=bool, default = False)
parser.add_argument("-wl", "--watlimit", dest = "watlim", action = "store", type=float, default = 60)
parser.add_argument("-b", dest = "Bchoice", action = "store", type=bool, default = False)
parser.add_argument("-bs", dest = "ObString", action = "store")
parser.add_argument("-ws", "--windowsize", dest = "WS", type=int, action = "store", default = 100)
parser.add_argument("-c", dest = "palette", action = "store", default = "Blues_r")
parser.add_argument("-lt", dest = "LastTime", action = "store", type=int, default = 1800)
parser.add_argument("-dc", dest = "d_col", action = "store", type=int, default = 1)
parser.add_argument("-EP", dest = "EP", action = "store", type=bool, default = False)
parser.add_argument("-obs", dest = "Obschoice", action = "store", type=bool, default = False)

args = parser.parse_args()
def ObsPlot(system,outname,colnum):
    UList = glob(system+"*.U.obs")
    LList = glob(system+"*.L.obs")
    UList.sort()
    LList.sort()
    FinalU, FinalL = [[],[],[]], [[],[],[]]
    label = 0
    for Ufile, Lfile in zip(UList,LList):
        with open(Ufile, 'r') as UF:
            U_all_lines = UF.read().splitlines()
        with open(Lfile, 'r') as LF:
            L_all_lines = LF.read().splitlines()
        for Uline, Lline in zip(U_all_lines,L_all_lines):
            if Uline.split()[0] == "Chain:":
                pass
            else:
                FinalU[0].append(float(Uline.split()[0])/10)
                FinalU[1].append(float(Uline.split()[colnum]))
                FinalU[2].append(label)
            if Lline.split()[0] == "Chain:":
                pass
            else:
                FinalL[0].append(float(Lline.split()[0])/10)
                FinalL[1].append(float(Lline.split()[colnum]))
                FinalL[2].append(label)
        label += 1
    UObsDF = pd.DataFrame({"Time (ns)": FinalU[0], "Obs": FinalU[1]})
    LObsDF = pd.DataFrame({"Time (ns)": FinalL[0], "Obs": FinalL[1]})
    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    np.set_printoptions(precision=3)
    plt.xlabel("Obs")
    ax.set_ylabel("Probability Mass Function")
    ax = sns.histplot(data=UObsDF,x="Obs",stat='density',label='Upper',legend=False,color="#7400B8")
    ax = sns.histplot(data=LObsDF,x="Obs",stat='density',label='Lower',legend=False,color="#80FFDB")
    ax2.set_ylabel("Cumulative Distribution Function")
    #ax2 = sns.ecdfplot(data=UObsDF,x="Obs",stat='proportion',color="#5E60CE")
    #ax2 = sns.ecdfplot(data=LObsDF,x="Obs",stat='proportion',color="#64DFDF")
    fig.legend()
    plt.savefig(outname+"_LvsU_Obs.png", dpi=400)
    plt.clf()

def WatFluxTrack(system,outname,palette,WS,LT,d_col,watlim,EP):
    WinS = int(WS)*10
    FileList = glob(system+"*WatFlux*")
    FileList.sort()
    print(FileList)
    # Final[i]: [[time] [instant Permeations] [cum. permeations] [label] [Average Flux] [instant current]]
    Final  = [[[],[],[],[],[],[]],[[],[],[],[],[],[]],[[],[],[],[],[],[]],[[],[],[],[],[],[]],[[],[],[],[],[],[]]]
    WinAVG = [[[],[],[],[]],[[],[],[],[]],[[],[],[],[]],[[],[],[],[]],[[],[],[],[]]]
    labels = []
    for i in range(len(FileList)):
        if EP == True:
            labels.append("Water")
        else:
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
                    Final[z][1].append(int(line.split()[z+1]))
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
            # Separate to calculate windowed-averages
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
            for n in HoldSep:
                for i in range(len(n)-WinS):
                    WinAVG[z][0].append(Final[z][0][i])
                    hold = []
                    for j in range(WinS):
                        hold.append(float(n[i+j]))
                    WinAVG[z][1].append(np.mean(hold))
                    WinAVG[z][2].append(z)
        with open(outname+f'_WA.txt', 'w') as out:
            for i in range(len(WinAVG[z][0])):
                out.write(f"{WinAVG[0][0][i]}\t{WinAVG[0][1][i]}\t{WinAVG[1][1][i]}\t{WinAVG[2][1][i]}\t{WinAVG[3][1][i]}\t{WinAVG[4][1][i]}\n")
        with open(outname+f"_CA.txt", 'w') as out:
            out.write(f"Time (ns)\tz = 45\tz = 30\tz = 0\tz = -30\tz = -45\n")
            for i in range(1,15):
                out.write(f"{Final[0][0][-(i*10)]}\t{Final[0][4][-(i*10)]}\t{Final[1][4][-(i*10)]}\t{Final[2][4][-(i*10)]}\t{Final[3][4][-(i*10)]}\t{Final[4][4][-(i*10)]}\n")

        CumPermeations  = [[],[],[]]
        CumAverage      = [[],[],[]]
        WindowAverage   = [[],[],[]]
        zables          = [" 45 Å"," 30 Å","  0 Å","-30 Å","-45 Å"]
        for z in range(5):
            for i in range(len(Final[0][0])):
                CumPermeations[0].append(Final[0][0][i])
                CumPermeations[1].append(Final[z][2][i])
                CumPermeations[2].append(zables[z])
                CumAverage[0].append(Final[0][0][i])
                CumAverage[1].append(Final[z][4][i])
                CumAverage[2].append(zables[z])
            for i in range(len(WinAVG[0][0])):
                WindowAverage[0].append(WinAVG[0][0][i])
                WindowAverage[1].append(WinAVG[z][1][i])
                WindowAverage[2].append(zables[z])
        CumPermeationsDF    = pd.DataFrame({"Time (ns)": CumPermeations[0], "Cumulative Permeations": CumPermeations[1], "Pore Height": CumPermeations[2]})
        CumAverageDF        = pd.DataFrame({"Time (ns)": CumAverage[0], "Cumulative Average": CumAverage[1], "Pore Height": CumAverage[2]})
        WindowAverageDF     = pd.DataFrame({"Time (ns)": WindowAverage[0], "Windowed Average Flux (ns^-1)": WindowAverage[1], "Pore Height": WindowAverage[2]})
        # Plot DataFrame
        plt.xlabel("Time (ns)")
        plt.ylabel('Windowed Avg. Water Flux (ns^-1)')
        sns.lineplot(data=WindowAverageDF, x="Time (ns)", y="Windowed Average Flux (ns^-1)", hue="Pore Height", palette=sns.color_palette(palette, n_colors=5))
        plt.savefig(outname+"_WinWatFlux.png", dpi=400)
        plt.clf()
        sns.displot(data=WindowAverage[1], kind="kde")
        plt.xlim(-(args.watlim),args.watlim)
        plt.ylim(0,0.05)
        plt.savefig(outname+"_flux-hist.png", dpi=400)
        plt.clf()
        fig, ax = plt.subplots()
        plt.xlabel("Time (ns)")
        plt.ylabel('Cumulative Water Permeations')
        sns.lineplot(data=CumPermeationsDF, x="Time (ns)", y="Cumulative Permeations", hue="Pore Height", palette=sns.color_palette(palette, n_colors=5))
        plt.savefig(outname+"_CumWaterPerm.png", dpi=400)
        plt.clf()
        fig, ax = plt.subplots()
        plt.ylim(-10,10)
        plt.xlabel("Time (ns)")
        plt.ylabel("Cumulative Avg. Water Flux (ns^-1)")
        sns.lineplot(data=CumAverageDF, x="Time (ns)", y="Cumulative Average", hue="Pore Height", palette=sns.color_palette(palette, n_colors=5))
        plt.savefig(outname+"_CumWaterFlux.png", dpi=400)
        plt.clf()
        return WindowAverage


if args.Pchoice == True:

    PMFPlotter(args.datstring,args.outname,args.palette)

if args.Tchoice == True:

    IonWindow = TrackerPlot(args.datstring,0,args.outname,args.palette,args.WS,args.Bchoice,args.LastTime,args.d_col,args.ObString,args.EP)

if args.Wchoice == True:

    WatWindow = WatFluxTrack(args.datstring,args.outname,args.palette,args.WS,args.LastTime,args.d_col,args.watlim,args.EP)

    if args.Wchoice == True and args.Tchoice == True:
        Final = [[],[]]
        watx, waty = Interp(WatWindow[0],WatWindow[1],args.LastTime)
        print(watx)
        #print(IonWindow[0])
        for i in range(len(IonWindow[0])):
            Final[0].append(waty[i])
            Final[1].append(IonWindow[1][i])
        FinalDF = pd.DataFrame({"Time (ns)": IonWindow[0], "Water Flux (ns^-1)": Final[0], "Ionic Current (pA)": Final[1]})
        plt.xlabel("Water Flux (ns^-1)")
        plt.ylabel("Current (pA)")
        sns.displot(data=FinalDF, x="Water Flux (ns^-1)", y="Ionic Current (pA)", kind='kde')
        plt.savefig(args.outname+"_WatVsCurr_hmap.png")
        plt.clf()

        fig, ax = plt.subplots()
        ax2 = ax.twinx()
        plt.title("Water & Ionic Flux")
        plt.xlabel("Time (ns)")
        ax = sns.lineplot(data=FinalDF,x="Time (ns)",y="Water Flux (ns^-1)",ax=ax,color="#00A6ED",label='Water',legend=False,linewidth=1)
        ax2 = sns.lineplot(data=FinalDF,x="Time (ns)",y="Ionic Current (pA)",ax=ax2,color="#F6511D",label='K+',legend=False,linewidth=1)
        fig.legend()
        plt.savefig(args.outname+"_WatVsCurr_line.png", dpi=400)
        plt.clf()
if args.Obschoice == True:

    ObsPlot(args.datstring,args.outname,args.d_col)
