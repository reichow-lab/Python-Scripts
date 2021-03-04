import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from glob import glob
from sys import argv
import pandas as pd
from scipy.interpolate import interp1d
#script, system, start, outname, palette, WS, obs = argv
def TrackerPlot(system,start,outname,palette,WS,obs):
    if bool(obs) == True:
        ObsFileList = glob("*.obs.txt")
        ObsFileList.sort()
    WinS = int(WS)
    FileList = glob(system)
    FileList.sort()
    # Final: [time] [cum. permeations] [label] [hue] [Average Current]
    Final = [[],[],[],[],[],[]]
    labels, hues = [],[]
    elemC,convF = 1.60217662e-19,(1e-9/1e-12)
    for i in range(len(FileList)):
        hues.append(i)
        labels.append(input("Label? "))
    # Import Data and interpolate. Also import the dts
    # fpt or First Passage Time (properly the first transition time)
    fptList = [[],[]]
    for FILE,label,hue in zip(FileList,labels,hues):
        with open(FILE, 'r') as file:
            Semi = [[],[],[],[],[]]
            for line in file:
                val = line.split()
                if val[0] == "Time":
                    pass
                elif val[0] == "Total" or val[0] == "Last":
                    pass
                elif val[0] < start:
                    pass
                else:
                    Semi[0].append(float(val[0]))
                    Semi[1].append(int(val[2]))
                    Semi[2].append(str(label))
                    Semi[3].append(int(hue))
                    if float(val[0]) <= 0:
                        pA = 0
                    elif float(val[0]) > 0:
                        pA = (int(val[2])*elemC)/(float(val[0])*1e-9)/(1e-12)
                    Semi[4].append(pA)
                    fptList[0].append(float(val[1]))
                    fptList[1].append(0)
            f = interp1d(Semi[0],Semi[1],kind="previous")
            # Process the interpolated data
            xnew = np.arange(0,int(Semi[0][-1]),1)
            ynew = f(xnew)
            for i in range(len(xnew)):
                Final[0].append(float(xnew[i]))
                Final[1].append(int(ynew[i]))
                Final[2].append(str(label))
                Final[3].append(int(hue))
                if i == 0:
                    Final[4].append(0)
                # Calculate instantaneous Slopes
                else:
                    Curr = float((ynew[i]-ynew[i-1])/(xnew[i]-xnew[i-1]))
                    Final[4].append(Curr)
                # Calculate Cumulative Current
                if xnew[i] <= 0:
                    pA = 0
<<<<<<< HEAD
                elif float(val[0]) > 0:
                    pA = (int(val[2])*elemC)/(float(val[0])*1e-9)/(1e-12)
                Semi[4].append(pA)
                fptList[0].append(float(val[1]))
                fptList[1].append(0)
        f = interp1d(Semi[0],Semi[1],kind="previous")
        # Process the interpolated data
        xnew = np.arange(0,1800,1)
        ynew = f(xnew)
        for i in range(len(xnew)):
            Final[0].append(float(xnew[i]))
            Final[1].append(int(ynew[i]))
            Final[2].append(str(label))
            Final[3].append(int(hue))
            if i == 0:
                Final[4].append(0)
            # Calculate instantaneous Slopes
            else:
                Curr = float((ynew[i]-ynew[i-1])/(xnew[i]-xnew[i-1]))
                Final[4].append(Curr)
            # Calculate Cumulative Current
            if xnew[i] <= 0:
                pA = 0
            elif xnew[i] > 0:
                pA = (int(ynew[i])*elemC)/(float(xnew[i])*1e-9)/(1e-12)
            Final[5].append(pA)
# Separate to calculate window-averages
HoldSep = []
for i in range(len(FileList)):
    HoldSep.append([])
n = -1
for i in range(len(Final[0])):
    if float(Final[0][i]) <= 0:
        n += 1
    HoldSep[n].append(Final[4][i])
# WinAvg: Time  Current  Hue  Label
WinAvg = [[],[],[],[]]
h = 0
for n in HoldSep:
    for i in range(len(n)-WinS):
        WinAvg[0].append(Final[0][i])
        hold = []
        for j in range(WinS):
            hold.append(float(n[i+j]))
        WinAvg[1].append(np.mean(hold)*160)
        WinAvg[2].append(h)
        WinAvg[3].append(labels[h])
    h += 1
# Perform the same data formatting for the new observable such that it has the same window averaging as the current
Obs = [[],[]]
for FILE in ObsFileList:
    with open(FILE, 'r') as file:
        Semi = [[],[]]
        for line in file:
            val = line.split()
            if val[0] == "Time":
                pass
            elif val[0] == "Total" or val[0] == "Last":
                pass
            else:
                Semi[0].append(float(val[0])/10)
                Semi[1].append(float(val[1]))
        f = interp1d(Semi[0],Semi[1],kind="previous")
        # Process the interpolated data
        xnew = np.arange(0,1800,1)
        ynew = f(xnew)
        for i in range(len(xnew)):
            Obs[0].append(float(xnew[i]))
            Obs[1].append(int(ynew[i]))
# Separate to calculate window-averages
HoldSep = []
for i in range(len(FileList)):
    HoldSep.append([])
n = -1
for i in range(len(Obs[0])):
    if float(Obs[0][i]) <= 0:
        n += 1
    HoldSep[n].append(Obs[1][i])
# WinAvg: Time  Current  Hue  Label
WinObs = [[],[],[],[]]

for n in HoldSep:
    for i in range(len(n)-WinS):
        WinObs[0].append(Obs[0][i])
        hold = []
        for j in range(WinS):
            hold.append(float(n[i+j]))
        WinObs[1].append(np.mean(hold))
################################################################################
plot_data1 = pd.DataFrame({"Time (ns)": Final[0], "Ion Permeations": Final[1]})
plot_data2 = pd.DataFrame({"Time (ns)": WinAvg[0], "current (pA)": WinAvg[1]})
plot_data3 = pd.DataFrame({"Time (ns)": Final[0], "<current> (pA)": Final[5]})
plot_data4 = pd.DataFrame({"First-Passage Times (ns)": fptList[0]})
if bool(obs) == True:
    print(len(WinAvg[1]),len(WinObs[1]))
    fig, ax1 = plt.subplots()
    plot_data5 = pd.DataFrame({"Current (pA)": WinAvg[1], "Observable": WinObs[1]})
    plt.title("Current vs. Observable")
    plt.xlabel("Current")
    plt.ylabel("Observable")
    #ax1 = sns.displot(plot_data5, x="Current (pA)", y="Observable", kind="kde")
    ax1 = sns.scatterplot(data=plot_data5, x="Current (pA)", y="Observable", linewidth=0, color="Grey")
    plt.savefig(outname+"_ObsVsCurr.png", dpi=400)
    plt.clf()
#plt.xlim(0,260)
#plt.ylim(0,200)
fig, ax1 = plt.subplots()
plt.title("Current")
plt.xlabel("Time (ns)")
plt.ylabel('Windowed Avg. Current (pA)')
ax1 = sns.lineplot(data=plot_data2, x="Time (ns)", y="current (pA)", hue=WinAvg[3], palette=sns.color_palette(palette, n_colors=len(FileList)))
plt.savefig(outname+"_current.png", dpi=400)
plt.clf()
#plt.xlim(0,260)
#plt.ylim(0,500)
#sns.set_palette(palette, 4)
fig, ax1 = plt.subplots()
plt.title("Flux")
plt.xlabel("Time (ns)")
plt.ylabel('Ion Permeations')
ax1 = sns.lineplot(data=plot_data1, x="Time (ns)", y="Ion Permeations", hue=Final[2], palette=sns.color_palette(palette, n_colors=len(FileList)))
plt.savefig(outname+"_flux.png", dpi=400)
plt.clf()
#sns.set_palette(palette, 4)
fig, ax1 = plt.subplots()
plt.title("Cumulative Current")
plt.xlabel("Time (ns)")
plt.ylabel("Running Avg. Current")
sns.lineplot(data=plot_data3, x="Time (ns)", y="<current> (pA)", hue=Final[2], palette=sns.color_palette(palette, n_colors=len(FileList)))
plt.savefig(outname+"_CumCurrent.png", dpi=400)
plt.clf()
np.set_printoptions(precision=3)
plt.title("First-Passage Times")
plt.xlabel("First Passage Times (ns)")
plt.ylabel("Probability Mass Function")
fig, ax1 = plt.subplots()
ax1.set_xlabel("First Transition Time")
ax1.set_ylabel("CDF")
plt.ylim(0,1)
ax1 = sns.ecdfplot(data=plot_data4,linewidth=2,palette=sns.color_palette("Greys", n_colors=1))
ax2 = ax1.twinx()
ax2.set_ylabel("PDF")
ax2 = sns.histplot(data=plot_data4,stat='density',palette=sns.color_palette(palette, n_colors=1))
plt.savefig(outname+"_FPT.png", dpi=400)
=======
                elif xnew[i] > 0:
                    pA = (int(ynew[i])*elemC)/(float(xnew[i])*1e-9)/(1e-12)
                Final[5].append(pA)
    # Separate to calculate window-averages
    HoldSep = []
    for i in range(len(FileList)):
        HoldSep.append([])
    n = -1
    for i in range(len(Final[0])):
        if float(Final[0][i]) <= 0:
            n += 1
        HoldSep[n].append(Final[4][i])
    # WinAvg: Time  Current  Hue  Label
    WinAvg = [[],[],[],[]]
    h = 0
    for n in HoldSep:
        for i in range(len(n)-WinS):
            WinAvg[0].append(Final[0][i])
            hold = []
            for j in range(WinS):
                hold.append(float(n[i+j]))
            WinAvg[1].append(np.mean(hold)*160)
            WinAvg[2].append(h)
            WinAvg[3].append(labels[h])
        h += 1
    # Perform the same data formatting for the new observable such that it has the same window averaging as the current
    Obs = [[],[]]
    for FILE in ObsFileList:
        with open(FILE, 'r') as file:
            Semi = [[],[]]
            for line in file:
                val = line.split()
                if val[0] == "Time":
                    pass
                elif val[0] == "Total" or val[0] == "Last":
                    pass
                else:
                    Semi[0].append(float(val[0]))
                    Semi[1].append(float(val[1]))
            f = interp1d(Semi[0],Semi[1],kind="previous")
            # Process the interpolated data
            xnew = np.arange(0,int(Semi[0][-1]),1)
            ynew = f(xnew)
            for i in range(len(xnew)):
                Obs[0].append(float(xnew[i]))
                Obs[1].append(int(ynew[i]))
    # Separate to calculate window-averages
    HoldSep = []
    for i in range(len(FileList)):
        HoldSep.append([])
    n = -1
    for i in range(len(Obs[0])):
        if float(Obs[0][i]) <= 0:
            n += 1
        HoldSep[n].append(Obs[1][i])
    # WinAvg: Time  Current  Hue  Label
    WinObs = [[],[],[],[]]

    for n in HoldSep:
        for i in range(len(n)-WinS):
            WinObs[0].append(Obs[0][i])
            hold = []
            for j in range(WinS):
                hold.append(float(n[i+j]))
            WinObs[1].append(np.mean(hold))
    ################################################################################
    plot_data1 = pd.DataFrame({"Time (ns)": Final[0], "Ion Permeations": Final[1]})
    plot_data2 = pd.DataFrame({"Time (ns)": WinAvg[0], "current (pA)": WinAvg[1]})
    plot_data3 = pd.DataFrame({"Time (ns)": Final[0], "<current> (pA)": Final[5]})
    plot_data4 = pd.DataFrame({"First-Passage Times (ns)": fptList[0]})
    if bool(obs) == True:
        print(len(WinAvg[1],len(WinObs)))
        plot_data5 = pd.DataFrame({"Current (pA)": WinAvg[1], "Observable": WinObs[1]})
        plt.title("Current vs. Observable")
        plt.xlabel("Current")
        plt.ylabel("Observable")
        plt.distplot(data=plot_data5, x="Current (pA)", y="Observable", kind="kde")
        plt.savefig(outname+"_ObsVsCurr.png")
    #plt.xlim(0,260)
    #plt.ylim(0,200)
    plt.title("Current")
    plt.xlabel("Time (ns)")
    plt.ylabel('Windowed Avg. Current (pA)')
    sns.lineplot(data=plot_data2, x="Time (ns)", y="current (pA)", hue=WinAvg[3], palette=sns.color_palette(palette, n_colors=len(FileList)))
    plt.savefig(outname+"_current.png", dpi=400)
    plt.clf()
    #plt.xlim(0,260)
    #plt.ylim(0,500)
    #sns.set_palette(palette, 4)
    plt.title("Flux")
    plt.xlabel("Time (ns)")
    plt.ylabel('Ion Permeations')
    sns.lineplot(data=plot_data1, x="Time (ns)", y="Ion Permeations", hue=Final[2], palette=sns.color_palette(palette, n_colors=len(FileList)))
    plt.savefig(outname+"_flux.png", dpi=400)
    plt.clf()
    #sns.set_palette(palette, 4)
    plt.title("Cumulative Current")
    plt.xlabel("Time (ns)")
    plt.ylabel("Running Avg. Current")
    sns.lineplot(data=plot_data3, x="Time (ns)", y="<current> (pA)", hue=Final[2], palette=sns.color_palette(palette, n_colors=len(FileList)))
    plt.savefig(outname+"_CumCurrent.png", dpi=400)
    plt.clf()
    np.set_printoptions(precision=3)
    plt.title("First-Passage Times")
    plt.xlabel("First Passage Times (ns)")
    plt.ylabel("Probability Mass Function")
    sns.histplot(data=plot_data4,stat='density',kde=True,palette=sns.color_palette(palette, n_colors=1))
    plt.savefig(outname+"_FPT.png", dpi=400)
>>>>>>> aaae19447b4afc85e05a2859cee18a7cc423c0db
